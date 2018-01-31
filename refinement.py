#!/usr/bin/env python
# module REFINEMENT
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

DEBUG = False
t0 = 0.1

def y_matlab2python(matlab_y, all_max=1):
    y_min = 16.0 / all_max
    y_max = 235.0 / all_max
    result = matlab_y.copy()
    result = (result - y_min) / (y_max - y_min) * (255 / all_max)
    return result

def y_python2matlab(python_y, all_max=1):
    y_min = 16.0 / all_max
    y_max = 235.0 / all_max
    result = python_y.copy()
    result = y_min + result * (y_max - y_min) / (255.0 / all_max)
    return result

def matlab2python(matlab_ycrcb, all_max=1):
    '''
    In matlab, ycrcb goes from
    16 to 235 in Y and 16 to 240 in Cr, Cb.
    in python, they cover the whole range of 0 to 255.
    '''
    y_min = 16.0 / all_max
    y_max = 235.0 / all_max
    c_min = 16.0 / all_max
    c_max = 240.0 / all_max
    result = matlab_ycrcb.copy()
    result[..., 0] = (result[:, :, 0] - y_min) / \
        (y_max - y_min) * (255 / all_max)
    result[..., 1] = (result[:, :, 1] - c_min) / \
        (c_max - c_min) * (255 / all_max)
    result[..., 2] = (result[:, :, 2] - c_min) / \
        (c_max - c_min) * (255 / all_max)
    return result


def python2matlab(python_ycrcb, all_max=1):
    y_min = 16.0 / all_max
    y_max = 235.0 / all_max
    c_min = 16.0 / all_max
    c_max = 240.0 / all_max
    result = python_ycrcb.copy()
    result[..., 0] = y_min + result[:, :, 0] * \
        (y_max - y_min) / (255.0 / all_max)
    result[..., 1] = c_min + result[:, :, 1] * \
        (c_max - c_min) / (255.0 / all_max)
    result[..., 2] = c_min + result[:, :, 2] * \
        (c_max - c_min) / (255.0 / all_max)
    return result


def get_vegetation_masks(red, nir):
    assert np.max(nir) <= 1.0 and np.min(nir) >= 0.0, "nir not between 0 and 1"
    assert np.max(red) <= 1.0 and np.min(red) >= 0.0, "red not between 0 and 1"

    Delta = np.subtract(nir, red)
    avg_Delta = Delta.mean()
    std_Delta = Delta.std()

    ### Normalization ###

    vegetationN = Delta > t0
    veg_estimate = np.sum(vegetationN)
    p = 100 * veg_estimate / Delta.size
    
    DeltaZ = np.divide((Delta - avg_Delta), std_Delta)
    if (DEBUG):
        fig, ax = plt.subplots(1, 3)
        ax[0].imshow(red)
        ax[0].set_title('red')
        ax[1].imshow(nir)
        ax[1].set_title('nir')
        ax[2].imshow(nir_sub_red)
        ax[2].set_title('diff')

    #from the examples use 1.5 when 0% vegetation and 0 when 100%
    v_min = 0
    v_max = 1.5
    Z_min = 0
    Z_max = 100
    #Z_thres = (veg_perc - v_min) * (v_min - v_max) / (Z_max - Z_min) + v_max
    t0Z = v_max - (p/Z_max)*v_max
    v_mask = DeltaZ > t0Z  # 0.65 for knoll

    v_prob = v_mask * DeltaZ
    M = np.max(v_prob)
    mNew = 0.5
    MNew = 1
    v_prob = v_prob*(MNew-mNew)/M + mNew
    v_prob = v_prob * v_mask

    if (DEBUG):
        print('Z:', t0Z)
        fig, ax = plt.subplots(1, 3)
        ax[0].imshow(vegetationN, cmap='gray')
        ax[0].set_title('vegetationN')
        ax[1].imshow(v_mask, cmap='gray')
        ax[1].set_title('v mask')
        ax[2].imshow(v_prob, cmap='gray')
        ax[2].set_title('v prob')
    return v_mask, v_prob


def ycc2rgb(Y_fused, matlab_color_ycc):
    matlab_fused_ycc = matlab_color_ycc
    # replace the color luma with the new one
    matlab_fused_ycc[:, :, 0] = Y_fused
    if (DEBUG):
        print('Yfused:', np.min(Y_fused), np.max(Y_fused))
    fused_ycc = matlab2python(matlab_fused_ycc, 255)
    # TODO why does it become yellow with fused_ycc and not with
    # matlab_fused_ycc?)
    fused = cv.cvtColor(matlab_fused_ycc, cv.COLOR_YCrCb2RGB)
    return fused


def apply_mask(color_bgr, dehazed_bgr, v_mask):
    '''
        returns dehazed_bgr with (weighted) pixels from color_bgr, wherever v_mask is not zero.
    '''
    assert np.max(color_bgr) > 1.0, "color not in (0,255)"
    assert np.max(dehazed_bgr) > 1.0, "dehazed not in (0,255)"

    color_ycc = (cv.cvtColor(color_bgr, cv.COLOR_BGR2YCrCb) /
                 255.0).astype(np.float32)
    dehazed_ycc = (cv.cvtColor(dehazed_bgr, cv.COLOR_BGR2YCrCb) /
                   255.0).astype(np.float32)
    matlab_color_ycc = python2matlab(color_ycc, 255.0)
    matlab_dehazed_ycc = python2matlab(dehazed_ycc, 255.0)
    Y_color = matlab_color_ycc[:, :, 0]
    Y_dehazed = matlab_dehazed_ycc[:, :, 0]
    Y_fused = Y_dehazed.copy()
    Y_fused[v_mask] = Y_color[v_mask]
    fused = ycc2rgb(Y_fused, matlab_color_ycc)
    return fused


def refine(color_bgr, dehazed_bgr, nir):
    ''' nir 2D matrix, color and dehazed (dehazed) 3D bgr matrices '''
    red = (color_bgr[:, :, 2]/255.0).astype(np.float32)
    v_mask, v_prob = get_vegetation_masks(red, nir)

    fused = apply_mask(color_bgr, dehazed_bgr, v_mask)
    return fused

if __name__ == "__main__":
    print('nothing happens when you run this module. Use its functions!')
