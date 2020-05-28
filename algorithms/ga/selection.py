from enum import Enum

import numpy as np

from utils.roulette import Roulette
from utils.multiobjective import nsga_ii_tourn


class Selection(Enum):
    RANDOM_SELECTION = 1
    ROULETTE_SELECTION = 2
    TOURNAMENT_SELECTION = 3
    NSGA_II_SELECTION = 4
    STOCHASTIC_SELECTION = 5
    TRUNCATION_SELECTION = 6


def selection_gene(population, survival_values, quant, method, config, **kwargs):
    parents = None

    if method == Selection.RANDOM_SELECTION:
        parents = _random_selection_gene(population, quant, **kwargs)

    elif method == Selection.ROULETTE_SELECTION:
        parents = _roulette_selection_gene(population, survival_values, quant, **kwargs)

    # elif method == Selection.TOURNAMENT_SELECTION:
    #     parents = _tournament_selection_gene(population, survival_values, quant, **kwargs)

    elif method == Selection.NSGA_II_SELECTION:
        parents = _nsga_ii_selection_gene(population, survival_values, quant, **kwargs)

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


# def _tournament_selection_gene(population, survival_values, quant, k):

def _nsga_ii_selection_gene(population, survival_values, quant, crowding_dist):
    parents_indexes = np.empty((quant,), dtype=int)

    tournament_indexes = np.random.randint(len(population), size=(quant, 2))
    for i in range(tournament_indexes.shape[0]):
        ind0 = tournament_indexes[i, 0]
        ind1 = tournament_indexes[i, 1]
        fit0 = survival_values[ind0]
        fit1 = survival_values[ind1]
        crowd_dist0 = crowding_dist[ind0]
        crowd_dist1 = crowding_dist[ind1]

        if nsga_ii_tourn(fit0, fit1, crowd_dist0, crowd_dist1) == 0:
            parents_indexes[i] = ind0
        else:
            parents_indexes[i] = ind1

    parents = population[parents_indexes]

    return parents


# def _stochastic_selection_gene(population, quant, config):
# def _truncation_selection_gene(population, quant, config):
