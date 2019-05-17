from enum import Enum

import numpy as np


class Copying(Enum):
    ELITISM_COPYING = 1
    PERMISSIVE_COPYING = 2
    NO_COPYING = 3


def copying_gene(population, method, config):
    new_population = None

    if (method == Copying.ELITISM_COPYING):
        new_population = _elitism_copying_gene(population, config)

    elif (method == Copying.PERMISSIVE_COPYING):
        new_population = _permissive_copying_gene(population, config)

    elif (method == Copying.NO_COPYING):
        new_population = _no_copying_gene(population, config)

    return new_population


def _elitism_copying_gene(population, config):
    top_selection_size = (int)(len(population) * config.top_selection_ratio)

    return np.copy(population[:top_selection_size])


def _permissive_copying_gene(population, config):
    top_selection_size = (int)(len(population) * config.top_selection_ratio)
    bottom_selection_size = (int)(len(population) * config.bottom_selection_ratio)

    return np.concatenate((population[:top_selection_size], population[population.shape[0] - bottom_selection_size:]))


def _no_copying_gene(population, args):
    return np.copy(population[:0])
