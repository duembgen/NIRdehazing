import matplotlib
#  matplotlib.use('Agg')
from multiresolution_decomposition import *
from registration import *
from pixel_fusion import *
import time
import cv2
import copy
from multiprocessing import Pool
from math import ceil


def dehaze(rgb_path, nir_path, dehazed_path, tile_width=100, tile_height=100, padding=5, n_jobs=4):
##   read images
    img_gray = cv2.imread(rgb_path, 0)
    img_rgb = cv2.cvtColor(cv2.imread(rgb_path), cv2.COLOR_RGB2LAB)
    img_lum = img_rgb[..., 0]
    img_nir_old = cv2.imread(nir_path)[..., 0]

##  image registration
    print('Registration...')
    img_nir = registration(img_gray, img_nir_old)
    cv2.imwrite('ispravena.png', img_nir)


##  parallel computations
    pool = Pool(processes=n_jobs)

##  create tiles
    nir_stack = decompose(img_nir, tile_width, tile_height, padding)
    rgb_stack = decompose(img_lum, tile_width, tile_height, padding)
    for i in rgb_stack:
        nir_stack.append(i)

    print('Analysis')
##  analysis for each image
    result = pool.map(multiresolution_analysis, nir_stack)

##  separate the results for the two images
    nir_result = []
    rgb_result = []
    n_rgb = len(rgb_stack)
    for i, r in enumerate(result):
        if i < n_rgb:
            nir_result.append(r)
        else:
            rgb_result.append(r)

##  prepare the arguments for the pixel fusion
    args = []
    for n, r in zip(nir_result, rgb_result):
        _, contrast = r
        _, contrast_nir = n
        args.append((contrast, contrast_nir))

    print('Pixel fusion')
##  pixel fusion for everz tile
    fused_stack = pool.map(pixel_fusion, args)

##  prepare arguments for the synthesis
    args = []
    for r, f in zip(rgb_result, fused_stack):
        base, _ = r
        args.append((base, f))

    print('synthezis')
##  synthezis for every tile
    image_stack = pool.map(multiresolution_synthesis, args)

##  recombine the tiles in a complete image
    x, y = img_lum.shape
    image = recombine(image_stack, padding, x, y)

##  Keep the color from the original and write the result
    img_rgb[..., 0] = np.round(image * 255)
    img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_LAB2RGB)
    cv2.imwrite(dehazed_path, img_rgb)
    print('Done')
