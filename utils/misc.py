import numpy as np


def hamming_distance(a, b, axis=None):
    if axis is None:
        return np.sum(a != b)
    else:
        return np.sum(a != b, axis=axis)


def get_integer(array):
    total = 0
    for shift, bit in enumerate(array[::-1]):
        total += bit * (1 << shift)
    return total


def get_float(array, bits_precision):
    total = 0
    for shift, bit in enumerate(array[::-1]):
        total += bit * (1 << shift)
    return (total / (1 << bits_precision))


def sigmoid(array):
    return 1 / (1 + np.exp(-array));
