import random

import numpy as np


def run_method(method_function, fitness_function, instance, config, num_repetitions, seed=0, **kwargs):
    best_fitness = []
    partial_fitness = []
    perf_counter = []
    process_time = []
    cost_value = []

    out_info = {}

    popularity = np.zeros((instance.num_materials,))

    for i in range(num_repetitions):
        np.random.seed(seed + i)
        random.seed(seed + i)
        (individual, survival_value) = method_function(instance, config, fitness_function, out_info=out_info, **kwargs)

        best_fitness.append(out_info["best_fitness"])
        partial_fitness.append(out_info["partial_fitness"])
        perf_counter.append(out_info["perf_counter"])
        process_time.append(out_info["process_time"])

        if len(out_info["cost_value"]) > len(cost_value):
            new_cost_values = out_info["cost_value"][len(cost_value):]
            cost_value.extend(new_cost_values)

        popularity += individual

    num_iterations = len(cost_value)

    best_fitness_array = np.zeros((num_repetitions, num_iterations))
    partial_fitness_array = np.zeros((num_repetitions, num_iterations, 5))
    perf_counter_array = np.zeros((num_repetitions, num_iterations))
    process_time_array = np.zeros((num_repetitions, num_iterations))

    for i in range(num_repetitions):
        repetition_len = len(best_fitness[i])

        best_fitness_array[i, :repetition_len] = best_fitness[i]
        partial_fitness_array[i, :repetition_len, :] = partial_fitness[i]
        perf_counter_array[i, :repetition_len] = perf_counter[i]
        process_time_array[i, :repetition_len] = process_time[i]

        best_fitness_array[i, repetition_len:] = best_fitness_array[i, repetition_len - 1]
        partial_fitness_array[i, repetition_len:] = partial_fitness_array[i, repetition_len - 1]
        perf_counter_array[i, repetition_len:] = perf_counter_array[i, repetition_len - 1]
        process_time_array[i, repetition_len:] = process_time_array[i, repetition_len - 1]

    # mean_best_fitness = np.mean(best_fitness_array, axis=0)
    # deviation_best_fitness = np.std(best_fitness_array, axis=0)
    # mean_perf_counter = np.mean(perf_counter_array, axis=0)
    # mean_process_time = np.mean(process_time_array, axis=0)

    # return (cost_value, mean_best_fitness, deviation_best_fitness, mean_perf_counter, mean_process_time)

    return (cost_value, best_fitness_array, partial_fitness_array, perf_counter_array, process_time_array)
