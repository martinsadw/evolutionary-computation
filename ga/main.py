import sys
import time
import math

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, fitness_population
from acs.instance import Instance, print_instance

from utils.timer import Timer

from ga.config import Config
from ga.copying import copying_gene
from ga.local_search import local_search_gene
from ga.selection import selection_gene
from ga.crossover import crossover_gene, Crossover
from ga.mutation import mutation_gene


cost_counter = 0
def counter_fitness(population, instance, timer, print_results=False, data=None):
    global cost_counter
    cost_counter += 1
    return fitness(population, instance, timer, print_results, data=data)


def genetic_algorithm(instance, config, fitness_function, out_info=None):
    population_size = config.population_size

    global cost_counter
    cost_counter = 0
    stagnation_counter = 0

    if out_info is not None:
        out_info["best_fitness"] = []
        out_info["perf_counter"] = []
        out_info["process_time"] = []
        out_info["cost_value"] = []

    timer = Timer()

    population = np.random.randint(2, size=(population_size, instance.num_materials), dtype=bool)
    population_best_individual = population[0]
    population_best_fitness = fitness_function(population[0], instance, timer)

    start_perf_counter = time.perf_counter()
    start_process_time = time.process_time()
    while (stagnation_counter < config.max_stagnation):
        timer.add_time()
        # print('==========================' + str(iteration))
        survival_values = np.apply_along_axis(fitness_function, 1, population, instance, timer)
        sorted_indices = np.argsort(survival_values)
        population = population[sorted_indices]
        survival_values = survival_values[sorted_indices]
        # print(survival_values)

        if survival_values[0] < population_best_fitness:
            population_best_individual = population[0]
            population_best_fitness = survival_values[0]

            stagnation_counter = 0
        else:
            stagnation_counter += 1

        if out_info is not None:
            # out_info["best_fitness"].append(survival_values[0])
            out_info["best_fitness"].append(population_best_fitness)
            out_info["perf_counter"].append(time.perf_counter() - start_perf_counter)
            out_info["process_time"].append(time.process_time() - start_process_time)
            out_info["cost_value"].append(cost_counter)

        new_population = copying_gene(population, config.copying_method, config)

        if config.use_local_search:
            new_population = local_search_gene(new_population, fitness_function, config.local_search_method, config)

        remaining_spots = np.random.randint(2, size=(population_size - new_population.shape[0], instance.num_materials), dtype=bool)
        remaining_spots = population_size - len(new_population)

        selection_spots = remaining_spots
        if (config.crossover_method == Crossover.THREE_PARENT_CROSSOVER):
            selection_spots = int(3 * math.ceil(remaining_spots / 3.)) * 3
        else:
            selection_spots = int(2 * math.ceil(remaining_spots / 2.))

        parents = selection_gene(population, survival_values, selection_spots, config.selection_method, config)
        children = crossover_gene(parents, config.crossover_method, config)
        mutated = mutation_gene(children, config.mutation_method, config)

        new_population = np.append(new_population, mutated[:remaining_spots], axis=0)
        population = new_population

    if out_info is not None:
        # out_info["best_fitness"].append(survival_values[0])
        out_info["best_fitness"].append(population_best_fitness)
        out_info["perf_counter"].append(time.perf_counter() - start_perf_counter)
        out_info["process_time"].append(time.process_time() - start_process_time)
        out_info["cost_value"].append(cost_counter)

    return (population, survival_values)


def read_files(instance_config_filename, config_filename):
    if instance_config_filename is None:
        instance = Instance.load_test()
    else:
        instance = Instance.load_from_file(instance_config_filename)

    if config_filename is None:
        config = Config.load_test()
    else:
        config = Config.load_from_file(config_filename)

    return (instance, config)


if __name__ == "__main__":
    instance_config_filename = None
    if (len(sys.argv) >= 2):
        instance_config_filename = sys.argv[1]

    config_filename = None
    if (len(sys.argv) >= 3):
        config_filename = sys.argv[2]

    num_repetitions = 10

    (instance, config) = read_files(instance_config_filename, config_filename)
    best_fitness = []
    perf_counter = []
    process_time = []
    cost_value = []

    out_info = {}

    popularity = np.zeros((instance.num_materials,))

    for i in range(num_repetitions):
        np.random.seed(i)
        (population, survival_values) = genetic_algorithm(instance, config, counter_fitness, out_info=out_info)

        best_fitness.append(out_info["best_fitness"])
        perf_counter.append(out_info["perf_counter"])
        process_time.append(out_info["process_time"])

        if len(out_info["cost_value"]) > len(cost_value):
            new_cost_values = out_info["cost_value"][len(cost_value):]
            cost_value.extend(new_cost_values)

        timer = Timer()
        fitness(population[0], instance, timer, True)

        popularity += population[0]

        print('#{}\n'.format(i))
        print('Survival values:\n{}\n'.format(survival_values))
        print('Best Individual:\n{}\n'.format(population[0]))

    num_iterations = len(cost_value)

    best_fitness_array = np.zeros((num_repetitions, num_iterations))
    perf_counter_array = np.zeros((num_repetitions, num_iterations))
    process_time_array = np.zeros((num_repetitions, num_iterations))

    for i in range(num_repetitions):
        repetition_len = len(best_fitness[i])

        best_fitness_array[i, :repetition_len] = best_fitness[i]
        perf_counter_array[i, :repetition_len] = perf_counter[i]
        process_time_array[i, :repetition_len] = process_time[i]

        best_fitness_array[i, repetition_len:] = best_fitness_array[i, repetition_len - 1]
        perf_counter_array[i, repetition_len:] = perf_counter_array[i, repetition_len - 1]
        process_time_array[i, repetition_len:] = process_time_array[i, repetition_len - 1]

    mean_best_fitness = np.mean(best_fitness_array, axis=0)
    deviation_best_fitness = np.std(best_fitness_array, axis=0)
    mean_perf_counter = np.mean(perf_counter_array, axis=0)
    mean_process_time = np.mean(process_time_array, axis=0)

    print('Statistics:')
    print('Fitness:\n{}\n'.format(mean_best_fitness))
    print('perf_counter:\n{}\n'.format(mean_perf_counter))
    print('process_time:\n{}\n'.format(mean_process_time))

    # fig = plt.figure()
    # fig.suptitle('PPA: perf_counter vs. process_time')
    # plt.plot(mean_perf_counter, 'r.')
    # plt.plot(mean_process_time, 'b.')
    # plt.show()

    fig = plt.figure()
    fig.suptitle('GA: best fitness')
    plt.plot(cost_value, mean_best_fitness, color='r')
    plt.plot(cost_value, mean_best_fitness+deviation_best_fitness, color='b', linewidth=0.5)
    plt.plot(cost_value, mean_best_fitness-deviation_best_fitness, color='b', linewidth=0.5)
    # plt.errorbar(cost_value, mean_best_fitness, yerr=deviation_best_fitness, color='r', ecolor='b')
    plt.show()

    # fig = plt.figure()
    # fig.suptitle('GA: materials selected')
    # plt.hist(popularity, bins=10, range=(0, num_repetitions))
    # plt.show()
