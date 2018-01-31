from wls_filter import wls_filter
import numpy as np


def multiresolution_analysis(image_orig, fil='wls', mode='haar', n=6, lambda_=0.1, c=2):
    """
    ARGs:
    ---------------------
    image:  0-255, uint8, single channel (e.g. grayscale or single L)
    n: number of levels in the multiresolution decomposition
    lambda_:
    c:
    fil: the type of wilter to use for the decomposition
    mode: If using the wavelet filter, the family of wavelet to use.
          see the available familise with pywt.wavelist()
    RETURN:
    ---------------------
    base_stack[n-1]: last level approximation image
    contrast_stack: contrast detailed decomposition of n levels
    """
    image = image_orig.astype(np.float) / 255.0
    base_stack = [image]
    contrast_stack = []

    lambda_c = lambda_

    for k in range(n):
        print('Iteration {} out of {}'.format(k + 1, n))
        if fil == 'wls':
            base = wls_filter(image_orig, lambda_c)
            lambda_c = lambda_c * c
        elif fil == 'wavelet':
            raise NotImplementedError('Wavelet decomposition not implemented yet.')
        else:
            raise ValueError(
                'The filter {} is not available. The available filters are wls and wavelet'.format(fil))

        contrast = np.divide((base_stack[k] - base), base + 1e-5)
        base_stack.append(base)
        contrast_stack.append(contrast)

    return base_stack[n], contrast_stack


def multiresolution_synthesis(args):
    """
    ARGs:
    ---------------------
    base: last level approximation image
    contrast_stack: contrast detailed decomposition of n levels

    RETURN:
    ---------------------
    output: reconstructed image
    """

    try:
        base, contrast_stack = args
    except Exception as e:
        print(e)

    output = base

    for contrast in contrast_stack:
        output = np.multiply(output, (contrast + 1))
        output = np.minimum(output, 1)

    return output


def recombine(stack, padding, width, height):
    from math import ceil
    n = len(stack)
    output = np.zeros((height, width))
    patch_height, patch_width = stack[0].shape
    patch_height = patch_height - 2 * padding
    patch_width = patch_width - 2 * padding
    columns = ceil(width / patch_width)
    rows = ceil(height / patch_height)

    for r in range(rows):
        row = r * patch_height
        for c in range(columns):
            column = c * patch_width
            index = r * columns + c
            if column + patch_width > width:
                left_width = width - column
            else:
                left_width = patch_width
            if row + patch_height > height:
                left_height = height - row
            else:
                left_height = patch_height
            output[row:row + left_height, column:column + left_width] = stack[index][padding:left_height + padding, padding:left_width + padding]
    return output


def decompose(image, width, height, padding):
    from math import ceil
    stack = []
    x, y = image.shape
    columns = ceil(y / height)
    rows = ceil(x / width)
    padded_image = np.pad(image, padding, 'edge')

    row = padding
    for r in range(rows):
        column = padding
        for c in range(columns):
            s = padded_image[row - padding:row + width + padding,
                             column - padding:column + height + padding]
            stack.append(s)
            column += height
        row += width
    return stack
