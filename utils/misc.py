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


def random_on_unit_sphere(shape, ndim):
    coord = np.random.normal(size=(shape + (ndim,)))
    normalized_coord = coord / vector_size(coord)[:, np.newaxis]
    return normalized_coord


def vector_size(vector, axis=-1):
    return np.sqrt(np.sum(vector ** 2, axis))


# def evaluate_population(population):
#     population_sigmoid = sigmoid(population)
#     population_random = np.random.random(population.shape)
#     population_evaluation = (population_sigmoid > population_random).astype(bool)
#
#     return population_evaluation


def evaluate_population(population):
    return (population > 0)


def improve_population(old_population, old_fitness, new_population, new_fitness):
    improve_mask = (new_fitness < old_fitness)
    best_population = np.where(improve_mask[:, np.newaxis], new_population, old_population)
    best_fitness = np.where(improve_mask, new_fitness, old_fitness)

    return (best_population, best_fitness)
