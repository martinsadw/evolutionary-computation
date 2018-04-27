import random

ELITISM_COPYING = 0
PERMISSIVE_COPYING = 1
NO_COPYING = 2


def copying_gene(population, method, args):
    new_population = []

    if (method == ELITISM_COPYING):
        new_population = _elitism_copying_gene(population, args)

    elif (method == PERMISSIVE_COPYING):
        new_population = _permissive_copying_gene(population, args)

    elif (method == NO_COPYING):
        new_population = _no_copying_gene(population, args)

    return new_population


def _elitism_copying_gene(population, args):
    assert 'top_selection_ratio' in args

    top_selection_size = (int)(len(population) * args['top_selection_ratio'])

    return population[:top_selection_size]


def _permissive_copying_gene(population, args):
    assert 'top_selection_ratio' in args
    assert 'bottom_selection_ratio' in args

    top_selection_size = (int)(len(population) * args['top_selection_ratio'])
    bottom_selection_size = (int)(len(population) * args['bottom_selection_ratio'])

    new_population = population[:top_selection_size]
    new_population.extend(population[-bottom_selection_size:])

    return new_population


def _no_copying_gene(population, args):
    return []
