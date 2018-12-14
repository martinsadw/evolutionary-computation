import random
from enum import Enum

import numpy as np


class LocalSearch(Enum):
    PER_VARIABLE_LOCAL_SEARCH = 1


def local_search_gene(population, fitness_function, method, config):
    new_population = None

    if (method == LocalSearch.PER_VARIABLE_LOCAL_SEARCH):
        new_population = _per_variable_local_search_gene(
            population, fitness_function, config)

    return new_population


def _per_variable_local_search_gene(population, fitness_func, args):
    # TODO(andre:2018-07-26): Adaptar a busca local para o algoritmo genetico
    return np.copy(population)

    # for gene in population:
    #     best_local_fitness = fitness_func(gene)
    #
    #     for name in gene.variables:
    #         best_variable_value = gene.get_value(name)
    #
    #         variable_value = best_variable_value
    #         variable_value -= (args['local_search_step'] * args['local_search_quant'] * 0.5)
    #
    #         for i in range(args['local_search_quant']):
    #             gene.set_value(name, variable_value)
    #
    #             new_local_fitness = fitness_func(gene)
    #             if new_local_fitness < best_local_fitness:
    #                 best_variable_value = variable_value
    #                 best_local_fitness = new_local_fitness
    #
    #             variable_value += args['local_search_step'] * i
    #
    #         gene.set_value(name, best_variable_value)


# def _multi_variable_local_search_gene(population, fitness_func, args):
# def _adaptive_local_search_gene(population, fitness_func, args):
