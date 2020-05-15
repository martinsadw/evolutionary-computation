import pickle

import numpy as np


def read_results(dataset, limit_size=100):
    # (instance, student, individual, function)
    with open(dataset, 'rb') as file:
        results = pickle.load(file)

    # Remove 'andre_50'
    results = results[1:, :, :, :]

    # (instance, student, individual, function)
    results = results[:, :, :limit_size, :]

    return results


def normalize_problem(data):
    # data = (instance, student, individual, function)

    # (instance, student, individual)
    total_sum_result = np.sum(data, axis=3)

    # (instance, student)
    min_sum_result = np.min(total_sum_result, axis=2)

    # (instance, student, 0, 0)
    min_sum_factor = min_sum_result[:, :, np.newaxis, np.newaxis]

    # (instance, student, individual, function)
    normalized_base_result = data / min_sum_factor

    return normalized_base_result


def normalize_objectives(data):
    # data = (instance, student, individual, function)

    # (function)
    max_objective = np.max(data, axis=(0, 1, 2))

    # (0, 0, 0, function)
    max_objective_factor = max_objective[np.newaxis, np.newaxis, np.newaxis, :]

    # (instance, student, individual, function)
    normalized_base_result = data / max_objective_factor

    return normalized_base_result


def normalized_fitness(dataset, limit_size=100):
    # (instance, student, individual, function)
    with open(dataset, 'rb') as file:
        results = pickle.load(file)

    # Remove 'andre_50'
    results = results[1:, :, :, :]

    # (instance, student, individual, function)
    total_base_result = results[:, :, :limit_size, :]

    # (instance, student, individual)
    total_sum_result = np.sum(total_base_result, axis=3)

    # (instance, student, 0, 0)
    min_sum_result = np.min(total_sum_result, axis=2)[:, :, np.newaxis, np.newaxis]

    # (instance, student, individual, function)
    normalized_base_result = total_base_result / min_sum_result

    return normalized_all_fitness


def normalized_objectives(dataset, limit_size=100):
    # (instance, student, individual, function)
    with open(dataset, 'rb') as file:
        results = pickle.load(file)

    # Remove 'andre_50'
    results = results[1:, :, :, :]

    # (instance, student, individual, function)
    results = results[:, :, :limit_size, :]

    # (instance, student, 0, function)
    max_sum_result = np.max(results, axis=2)[:, :, np.newaxis, :]
    max_sum_result[max_sum_result == 0] = 1

    # (instance, student, individual, function)
    results = results / max_sum_result

    return results


# def normalized_objectives(dataset, limit_size=100):
#     # (instance, student, individual, function)
#     with open(dataset, 'rb') as file:
#         results = pickle.load(file)
#
#     # Remove 'andre_50'
#     results = results[1:, :, :, :]
#
#     # Limit number of individuals
#     results = results[:, :, :limit_size, :]
#
#     # (instance, student, individual, function)
#     results = normalize_problem(results)
#
#     # (instance, student, individual, function)
#     results = normalize_objectives(results)
#
#     return results
