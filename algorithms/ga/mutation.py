import numpy as np

from enum import Enum


class Mutation(Enum):
    MULTI_BIT_INVERSION_MUTATION = 1
    SINGLE_BIT_INVERSION_MUTATION = 2


def mutation_gene(children, method, config):
    new_gene = np.copy(children)

    if (method == Mutation.MULTI_BIT_INVERSION_MUTATION):
        new_gene = _multi_bit_inversion_mutation_gene(children, config)
    if (method == Mutation.SINGLE_BIT_INVERSION_MUTATION):
        new_gene = _single_bit_mutation(children, config)
    return new_gene


def _multi_bit_inversion_mutation_gene(children, config):
    new_gene = np.copy(children)
    bitsize = children.shape[1]

    mask = np.random.rand(*children.shape) < config.mutation_chance
    new_gene ^= mask

    return new_gene


def _single_bit_mutation(children, config, bit=None):
    new_gene = np.copy(children)

    bitsize = children.shape[1]

    cut_point = np.random.randint(0, bitsize, size=children.shape[0])
    r = np.arange(bitsize)

    mask = cut_point[:, np.newaxis] == r
    new_gene ^= mask

    return new_gene
