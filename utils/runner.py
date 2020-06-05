import random

import numpy as np


def run_method(method_function, fitness_function, instance, config, num_repetitions, seed=0, result_format='simple', verbose=False, **kwargs):
    best_fitness = []
    partial_fitness = []
    perf_counter = []
    process_time = []
    cost_value = []

    out_info = {}

    selected_materials = np.zeros((num_repetitions, instance.num_learners, instance.num_materials), dtype=bool)

    for i in range(num_repetitions):
        if verbose:
            print('Progress: %d / %d (%d%%)' % (i + 1, num_repetitions, (i + 1) * 100 / num_repetitions))

        np.random.seed(seed + i)
        random.seed(seed + i)
        results = method_function(instance, config, fitness_function, out_info=out_info, **kwargs)

        for j, result in enumerate(results):
            selected_materials[i, j] = result[0]

        best_fitness.append(out_info["best_fitness"])
        partial_fitness.append(out_info["partial_fitness"])
        perf_counter.append(out_info["perf_counter"])
        process_time.append(out_info["process_time"])

        # NOTE(andre:2019-08-09): Considera que a lista de valores de custo
        # possuem sempre os mesmo valores para cada algoritmo mudando apenas o tamanho
        for student_cost_value in out_info["cost_value"]:
            if len(student_cost_value) > len(cost_value):
                new_cost_values = student_cost_value[len(cost_value):]
                cost_value.extend(new_cost_values)

    num_iterations = len(cost_value)

    best_fitness_array = np.zeros((num_repetitions, instance.num_learners, num_iterations))
    partial_fitness_array = np.zeros((num_repetitions, instance.num_learners, num_iterations, 5))
    perf_counter_array = np.zeros((num_repetitions, instance.num_learners, num_iterations))
    process_time_array = np.zeros((num_repetitions, instance.num_learners, num_iterations))

    for i in range(num_repetitions):
        for j in range(instance.num_learners):
            repetition_len = len(best_fitness[i][j])

            best_fitness_array[i, j, :repetition_len] = best_fitness[i][j]
            partial_fitness_array[i, j, :repetition_len, :] = partial_fitness[i][j]
            perf_counter_array[i, j, :repetition_len] = perf_counter[i][j]
            process_time_array[i, j, :repetition_len] = process_time[i][j]

            best_fitness_array[i, j, repetition_len:] = best_fitness_array[i, j, repetition_len - 1]
            partial_fitness_array[i, j, repetition_len:] = partial_fitness_array[i, j, repetition_len - 1]
            perf_counter_array[i, j, repetition_len:] = perf_counter_array[i, j, repetition_len - 1]
            process_time_array[i, j, repetition_len:] = process_time_array[i, j, repetition_len - 1]

    if result_format == 'simple':
        return (selected_materials, cost_value, partial_fitness_array)
    elif result_format == 'full':
        return (selected_materials, cost_value, best_fitness_array, partial_fitness_array, perf_counter_array, process_time_array)

    return None


def run_multiobjective_method(method_function, fitness_function, instance, config, num_repetitions, seed=0, result_format='simple', verbose=False, **kwargs):
    best_fitness = []
    population_fitness = []
    perf_counter = []
    process_time = []
    cost_value = []

    out_info = {}

    selected_materials = np.zeros((num_repetitions, instance.num_learners, config.population_size, instance.num_materials), dtype=bool)

    for i in range(num_repetitions):
        if verbose:
            print('Progress: %d / %d (%d%%)' % (i + 1, num_repetitions, (i + 1) * 100 / num_repetitions))

        np.random.seed(seed + i)
        random.seed(seed + i)
        results = method_function(instance, config, fitness_function, out_info=out_info, **kwargs)

        for j, result in enumerate(results):
            selected_materials[i, j] = result[0]

        best_fitness.append(out_info["best_fitness"])
        population_fitness.append(out_info["population_fitness"])
        perf_counter.append(out_info["perf_counter"])
        process_time.append(out_info["process_time"])

        # NOTE(andre:2019-08-09): Considera que a lista de valores de custo
        # possuem sempre os mesmo valores para cada algoritmo mudando apenas o tamanho
        for student_cost_value in out_info["cost_value"]:
            if len(student_cost_value) > len(cost_value):
                new_cost_values = student_cost_value[len(cost_value):]
                cost_value.extend(new_cost_values)

    num_iterations = len(cost_value)
    num_objectives = results[0][1][0].shape[0]  # results[learner][population|fitness][individual]

    best_fitness_array = np.zeros((num_repetitions, instance.num_learners, num_iterations))
    population_fitness_array = np.zeros((num_repetitions, instance.num_learners, num_iterations, config.population_size, num_objectives))
    perf_counter_array = np.zeros((num_repetitions, instance.num_learners, num_iterations))
    process_time_array = np.zeros((num_repetitions, instance.num_learners, num_iterations))

    for i in range(num_repetitions):
        for j in range(instance.num_learners):
            repetition_len = len(best_fitness[i][j])

            best_fitness_array[i, j, :repetition_len] = best_fitness[i][j]
            population_fitness_array[i, j, :repetition_len, :, :] = population_fitness[i][j]
            perf_counter_array[i, j, :repetition_len] = perf_counter[i][j]
            process_time_array[i, j, :repetition_len] = process_time[i][j]

            best_fitness_array[i, j, repetition_len:] = best_fitness_array[i, j, repetition_len - 1]
            population_fitness_array[i, j, repetition_len:] = population_fitness_array[i, j, repetition_len - 1]
            perf_counter_array[i, j, repetition_len:] = perf_counter_array[i, j, repetition_len - 1]
            process_time_array[i, j, repetition_len:] = process_time_array[i, j, repetition_len - 1]

    if result_format == 'simple':
        return (selected_materials, cost_value, population_fitness_array)
    elif result_format == 'full':
        return (selected_materials, cost_value, best_fitness_array, population_fitness_array, perf_counter_array, process_time_array)

    return None
