import numpy as np
from scipy.sparse import spdiags
from scipy.sparse.linalg import spsolve


def wls_filter(image_orig, lambda_=0.4, alpha=1.2, EPSILON=1e-6):
    """
    ARGs:
    -----
    image: 0-255, uint8, single channel (e.g. grayscale or single L)
    lambda_:
    alpha:
    RETURN:
    -----
    output: base, 0-1, float
    """

    image = image_orig.astype(float) / 255.0
    s = image.shape
    k = np.prod(s)

    dy = np.diff(np.log10(image + EPSILON), 1, 0)
    dy = -lambda_ / (np.absolute(dy) ** alpha + EPSILON)
    dy = np.vstack(
        (
            dy,
            np.zeros(
                s[1],
            ),
        )
    )
    dy = dy.flatten("F")

    dx = np.diff(np.log10(image + EPSILON), 1, 1)
    dx = -lambda_ / (np.absolute(dx) ** alpha + EPSILON)
    dx = np.hstack(
        (
            dx,
            np.zeros(
                s[0],
            )[:, np.newaxis],
        )
    )
    dx = dx.flatten("F")

    a = spdiags(np.vstack((dx, dy)), [-s[0], -1], k, k, format="csr")
    d = 1 - (dx + np.roll(dx, s[0]) + dy + np.roll(dy, 1))
    a = a + a.T + spdiags(d, 0, k, k, format="csr")

    output = spsolve(a, image.flatten(order="C"))
    output = np.rollaxis(output.reshape(s[::-1]), 1)

    return output
