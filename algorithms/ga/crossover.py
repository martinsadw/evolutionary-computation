import numpy as np

from enum import Enum


class Crossover(Enum):
    SINGLE_POINT_CROSSOVER = 1
    TWO_POINT_CROSSOVER = 2
    THREE_PARENT_CROSSOVER = 3
    UNIFORM_CROSSOVER = 4
    DECIMAL_CROSSOVER = 5


def crossover_gene(parents, method, config):
    children = None

    if method == Crossover.SINGLE_POINT_CROSSOVER:
        children = _single_point_crossover_gene(parents, config)

    elif method == Crossover.TWO_POINT_CROSSOVER:
        children = _two_point_crossover_gene(parents, config)

    elif method == Crossover.THREE_PARENT_CROSSOVER:
        children = _three_parent_crossover_gene(parents, config)

    elif method == Crossover.UNIFORM_CROSSOVER:
        children = _uniform_crossover_gene(parents, config)

    # elif method == Crossover.DECIMAL_CROSSOVER:
    #     precision = children.variables_descriptor['x'][2]
    #     children = _single_point_crossover_gene(parents, config, precision)

    return children


def _single_point_crossover_gene(parents, config, cut_point=None):
    assert parents.shape[0] % 2 == 0

    # Exemplo:
    # value1:         1101 0011
    # value2:         1001 1101

    # cut_point: 5

    # mask:           0001 1111

    # value1 & ~mask: 1100 0000
    # value2 &  mask: 0001 1101
    # result1:        1101 1101

    # value1 &  mask: 0001 0011
    # value2 & ~mask: 1000 0000
    # result2:        1001 0011

    # if cut_point is None:
    #     cut_point = random.randint(1, parents.shape[1])

    bitsize = parents.shape[1]

    if cut_point is None:
        cut_point = np.random.randint(0, bitsize, size=int(parents.shape[0] / 2))

    r = np.arange(bitsize)
    mask = cut_point[:, np.newaxis] >= r

    # mask = (1 << cut_point) - 1

    value1 = ((parents[::2] & ~mask) | (parents[1::2] &  mask)).astype(bool)
    value2 = ((parents[::2] &  mask) | (parents[1::2] & ~mask)).astype(bool)

    return np.concatenate((value1, value2))


def _two_point_crossover_gene(parents, config, cut_point1=None, cut_point2=None):
    assert parents.shape[0] % 2 == 0

    # Exemplo:
    # value1:         1101 0011
    # value2:         1001 1101

    # cut_point1: 3
    # cut_point2: 7

    # mask1:          0000 0111
    # mask2:          0111 1111
    # mask:           0111 1000

    # value1 & ~mask: 1000 0011
    # value2 &  mask: 0001 1000
    # result1:        1001 1011

    # value1 &  mask: 0101 0000
    # value2 & ~mask: 1000 0101
    # result2:        1101 0101

    bitsize = parents.shape[1]

    if(cut_point1 is None):
        cut_point1 = np.random.randint(0, bitsize, size=int(parents.shape[0] / 2))
    if(cut_point2 is None):
        cut_point2 = np.random.randint(0, bitsize, size=int(parents.shape[0] / 2))

    r = np.arange(bitsize)
    mask1 = cut_point1[:, np.newaxis] >= r
    mask2 = cut_point2[:, np.newaxis] >= r
    mask = mask1 ^ mask2

    value1 = ((parents[::2] & ~mask) | (parents[1::2] &  mask)).astype(bool)
    value2 = ((parents[::2] &  mask) | (parents[1::2] & ~mask)).astype(bool)

    return np.concatenate((value1, value2))


def _three_parent_crossover_gene(parents, config):
    assert parents.shape[0] % 3 == 0

    # Exemplo:
    # value1:         110100010
    # value2:         011001001
    # value3:         110110101

    # mask:           010010100

    # value1 &  mask: 010000000
    # value3 & ~mask: 100100001

    # result:         110100001

    mask = ~(parents[::3] ^ parents[1::3])  # seleciona os bits que sao iguais

    new_gene = ((parents[::3] & mask | parents[2::3] & ~mask))

    return new_gene


def _uniform_crossover_gene(parents, config):
    assert parents.shape[0] % 2 == 0

    # Exemplo:
    # value1:         1101 0011
    # value2:         1001 1101

    # mask:           0010 0110

    # value1 & ~mask: 1101 0001
    # value2 &  mask: 0000 0100

    # result:         1101 0101

    bitsize = parents.shape[1]

    mask = np.random.rand(*parents[::2].shape) < 0.5

    new_gene1 = ((parents[::2] & ~mask) | (parents[1::2] &  mask))
    new_gene2 = ((parents[::2] &  mask) | (parents[1::2] & ~mask))

    return np.concatenate((new_gene1, new_gene2))
