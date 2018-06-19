import numpy as np


def hamming_distance(a, b, axis=None):
    if axis is None:
        return np.sum(a != b)
    else:
        return np.sum(a != b, axis=axis)
