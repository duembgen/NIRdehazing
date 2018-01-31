import numpy as np
import matplotlib.pyplot as plt
from plots import plot_picture


def pixel_fusion(args, mask=None, print_out=False):
    """
    ARGs:
    ------------------------------------------------------
    list of tuples of type (rgb_constrast_stack, nir_contrast_stack)
    rgb_contrast_stack: stack containing the contrast images of different levels of the rgb image
    nir_contrast_stack: stack containing the contrast images of different levels of the nir image

    RETURN:
    -------------------------------------------------------
    fused_stack: contrast images fused at each level following the max criteria
    """

    try:
        rgb_contrast_stack, nir_contrast_stack = args
    except Exception as e:
        print(e)

    assert len(rgb_contrast_stack) == len(nir_contrast_stack), 'The length of the two contrast stacks should be the same'
    n = len(rgb_contrast_stack)

    fused_stack = []
    for rgb_contrast, nir_contrast in zip(rgb_contrast_stack, nir_contrast_stack):
        if mask is not None:
            min_nir = np.min(nir_contrast)
            min_rgb = np.min(rgb_contrast)
            min_ = min(min_nir, min_rgb)-1e-3
            mask_new = mask * min_
            if (print_out):
                plot_picture(mask_new, 'new mask')
            nir_contrast_new = nir_contrast.copy()
            nir_contrast_new[mask > 0] = mask_new[mask > 0]
        else:
            nir_contrast_new = nir_contrast
        fused = np.maximum(rgb_contrast, nir_contrast_new)
        fused_stack.append(fused)
        if (print_out):
            plot_picture(rgb_contrast, 'rgb contrast')
            plot_picture(nir_contrast, 'nir contrast')
            plot_picture(nir_contrast_new, 'nir contrast new')
            plot_picture(fused, 'fused')
    return fused_stack

