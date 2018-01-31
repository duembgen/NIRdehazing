import numpy as np
import matplotlib.pyplot as plt
import cv2
from multiresolution_decomposition import *
from registration import *

dryrun = False

filenames = [
    ['branchview','.tif'],
    ['knoll', '.tif']]

registration = False

for arg in filenames:
    filename, filetype = arg
    rgb_path = 'input/' + filename + filetype
    nir_path = 'input/' + filename + '_nir' + filetype
    print('reading images', rgb_path, nir_path)
    img_gray = cv2.imread(rgb_path, 0)
    img_bgr = cv2.imread(rgb_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    img_ycrcb = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2YCrCb)
    img_lum = img_lab[..., 0]
    img_nir_old = cv2.imread(nir_path)[..., 0]
    if not dryrun:
        print('image registration')
        if registration:
            img_nir = registration(img_gray, img_nir_old)
        else:
            img_nir = img_nir_old
        cv2.imwrite('output/' + filename + '_registered.png', img_nir)
        print('wls')
        nir_base, nir_detail = multiresolution_analysis(img_nir, n=6)
        rgb_base, rgb_detail = multiresolution_analysis(img_lum, n=6)
        for counter in range(len(nir_base)):
            np.save('output/{}_nir_base{}'.format(filename,
                                                  counter), nir_base[counter])
            np.save('output/{}_vis_base{}'.format(filename,
                                                  counter), rgb_base[counter])
        for counter in range(len(nir_detail)):
            np.save('output/{}_nir_detail{}'.format(filename,
                                                    counter), nir_detail[counter])
            np.save('output/{}_vis_detail{}'.format(filename,
                                                    counter), rgb_detail[counter])
