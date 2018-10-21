from enum import Enum

import numpy as np

from utl.roulette import Roulette


class Selection(Enum):
    RANDOM_SELECTION = 1
    ROULETTE_SELECTION = 2


def selection_gene(population, survival_values, quant, method, config):
    parents = None

    if method == Selection.RANDOM_SELECTION:
        parents = _random_selection_gene(population, quant)

    elif method == Selection.ROULETTE_SELECTION:
        parents = _roulette_selection_gene(population, survival_values, quant)

    return parents


def _random_selection_gene(population, quant):
    parents_indexes = np.random.randint(len(population), size=quant)
    parents = population[parents_indexes]

    return parents


def _roulette_selection_gene(population, survival_values, quant):
    # TODO(andre:2018-08-17): Rever a forma como as chances de escolher um gene são calculadas
    roulette = Roulette(1 / survival_values)

    parents_indexes = [roulette.spin() for i in range(quant)]
    parents = population[parents_indexes]

    return parents


# def _stochastic_selection_gene(population, quant, args):
# def _truncation_selection_gene(population, quant, args):
