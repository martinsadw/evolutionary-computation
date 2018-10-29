import random

import numpy as np

from enum import Enum


class Crossover(Enum):
    SINGLE_POINT_CROSSOVER = 1
    TWO_POINT_CROSSOVER = 2
    THREE_PARENT_CROSSOVER = 3
    UNIFORM_CROSSOVER = 4
    DECIMAL_CROSSOVER = 5


# def crossover_gene(parents, quant, method, config):
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

    if cut_point is None:
        #cut_point = np.random.randint(1, parents.shape[1] - 1, size=parents.shape[0]/2, dtype=bool)
        cut_point = random.randint(1, parents.shape[1] - 1)

    #mask = np.zeros((parents.shape[0]/2,parents.shape[1]))
    mask=(1 << cut_point+1)-1

    value1 = ((parents[::2] & ~mask) | (parents[1::2] & mask)).astype(bool)
    value2 = ((parents[::2] & mask) | (parents[1::2] & ~mask)).astype(bool)

    return np.concatenate((value1, value2))


def _two_point_crossover_gene(genes, args):
    assert len(genes) == 2

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

    new_gene1 = genes[0]
    new_gene2 = genes[0]

    for name in new_gene1.variables:
        bitsize = new_gene1.get_variable_size(name)

        value1 = genes[0].variables[name]
        value2 = genes[1].variables[name]

        # TODO(andre:2018-04-05): Garantir que os pontos de cortes sejam diferentes
        cut_point1 = random.randrange(1, bitsize)
        cut_point2 = random.randrange(1, bitsize)
        i = 0
        while cut_point1 == cut_point2 & i < 5:
            cut_point2 = random.randrange(1, bitsize)
            i += 1

        # e.g. 0000 0000 0011 1111 se cut_point1 = 6
        mask1 = (1 << cut_point1) - 1
        # e.g. 0000 0111 1111 1111 se cut_point2 = 11
        mask2 = (1 << cut_point2) - 1
        mask = (mask1 ^ mask2)         # e.g. 0000 0111 1100 0000

        new_gene1.variables[name] = (value1 & ~mask) | (value2 & mask)
        new_gene2.variables[name] = (value1 & mask) | (value2 & ~mask)

    return (new_gene1, new_gene2)


def _three_parent_crossover_gene(genes, args):
    assert len(genes) == 3

    # Exemplo:
    # value1:         110100010
    # value2:         011001001
    # value3:         110110101

    # mask:           010010100

    # value1 &  mask: 010000000
    # value3 & ~mask: 100100001

    # result:         110100001

    new_gene1 = genes[0]
    new_gene2 = genes[0]
    new_gene3 = genes[0]

    for name in new_gene1.variables:
        value1 = genes[0].variables[name]
        value2 = genes[1].variables[name]
        value3 = genes[2].variables[name]

        mask1 = ~(value1 ^ value2)  # seleciona os bits que sao iguais
        mask2 = ~(value2 ^ value3)
        mask3 = ~(value1 ^ value3)

        new_gene1.variables[name] = (value1 & mask1) | (
            value3 & ~mask1)  # usa o terceiro pai em caso de empate
        new_gene2.variables[name] = (value2 & mask2) | (value1 & ~mask2)
        new_gene3.variables[name] = (value3 & mask3) | (value2 & ~mask3)

    return (new_gene1, new_gene2, new_gene3)


def _uniform_crossover_gene(genes, args):
    assert len(genes) == 2

    # Exemplo:
    # value1:         1101 0011
    # value2:         1001 1101

    # mask:           0010 0110

    # value1 & ~mask: 1101 0001
    # value2 &  mask: 0000 0100

    # result:         1101 0101

    new_gene = genes[0]

    for name in new_gene.variables:
        value1 = genes[0].variables[name]
        value2 = genes[1].variables[name]
        bitsize = new_gene.get_variable_size(name)

        mask = 0
        for x in range(bitsize):
            if random.random() < 0.5:
                mask &= (1 << x)

        new_gene.variables[name] = (value1 & ~mask) | (value2 & mask)

    return (new_gene,)
