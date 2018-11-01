import sys
import time
import math

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, fitness_population
from acs.instance import Instance, print_instance

from utl.timer import Timer

from ga.config import Config, Crossover
from ga.copying import copying_gene
from ga.local_search import local_search_gene
from ga.selection import selection_gene
from ga.crossover import crossover_gene
from ga.mutation import mutation_gene


def genetic_algorithm(instance, config, fitness_function, *, best_fitness=None, perf_counter=None, process_time=None, all_fitness=None):
    population_size = config.population_size

    population = np.random.randint(
        2, size=(population_size, instance.num_materials), dtype=bool)

    timer = Timer()

    start_perf_counter = time.perf_counter()
    start_process_time = time.process_time()
    for iteration in range(config.num_iterations+1):
        timer.add_time()
        # print('==========================' + str(iteration))
        survival_values = np.apply_along_axis(
            fitness_function, 1, population, instance, timer, data=all_fitness)
        sorted_indices = np.argsort(survival_values)
        population = population[sorted_indices]
        survival_values = survival_values[sorted_indices]
        print(survival_values)

        if best_fitness is not None:
            best_fitness[iteration] = survival_values[0]
        if perf_counter is not None:
            perf_counter[iteration] = time.perf_counter() - start_perf_counter
        if process_time is not None:
            process_time[iteration] = time.process_time() - start_process_time

        new_population = copying_gene(
            population, config.copying_method, config)

        if config.use_local_search:
            new_population = local_search_gene(
                new_population, fitness_function, config.local_search_method, config)

        remaining_spots = np.random.randint(2, size=(
            population_size - new_population.shape[0], instance.num_materials), dtype=bool)
        remaining_spots = population_size - len(new_population)

        selection_spots = remaining_spots
        if (config.crossover_method == Crossover.THREE_PARENT_CROSSOVER):
            selection_spots = int(3 * math.ceil(remaining_spots / 3.)) * 3
        elif (config.crossover_method == Crossover.UNIFORM_CROSSOVER):
            selection_spots = int(2 * math.ceil(remaining_spots / 2.)) * 2
        else:
            selection_spots = int(2 * math.ceil(remaining_spots / 2.))

        parents = selection_gene(
            population, survival_values, selection_spots, config.selection_method, config)
        children = crossover_gene(parents, config.crossover_method, config)
        mutated = mutation_gene(children, config.mutation_method, config)

        new_population = np.append(new_population, mutated, axis=0)
        population = new_population

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

    num_repetitions = 1

    (instance, config) = read_files(instance_config_filename, config_filename)
    best_fitness = np.zeros((config.num_iterations + 1, num_repetitions))
    perf_counter = np.zeros((config.num_iterations + 1, num_repetitions))
    process_time = np.zeros((config.num_iterations + 1, num_repetitions))
    all_fitness = []

    popularity = np.zeros((instance.num_materials,))

    for i in range(num_repetitions):
        (population, survival_values) = genetic_algorithm(instance, config, fitness,
                                                          best_fitness=best_fitness[:, i], perf_counter=perf_counter[:, i], process_time=process_time[:, i], all_fitness=all_fitness)
        timer = Timer()
        fitness(population[0], instance, timer, True)
        popularity += population[0]
        print('#{}\n'.format(i))
        print('Survival values:\n{}\n'.format(survival_values))
        print('Best Individual:\n{}\n'.format(population[0]))
        print('Popularity:\n{}\n'.format(popularity))

    mean_best_fitness = np.mean(best_fitness, axis=1)
    mean_perf_counter = np.mean(perf_counter, axis=1)
    mean_process_time = np.mean(process_time, axis=1)

    print('Statistics:')
    print('Fitness:\n{}\n'.format(mean_best_fitness))
    print('perf_counter:\n{}\n'.format(mean_perf_counter))
    print('process_time:\n{}\n'.format(mean_process_time))

    print('Popularity:\n{}\n'.format(popularity))

    fig = plt.figure()
    fig.suptitle('GA: best fitness')
    plt.plot(mean_best_fitness, 'r')
    plt.show()

    fig = plt.figure()
    fig.suptitle('GA: materials selected')
    plt.hist(popularity, bins=10, range=(0, num_repetitions))
    plt.show()
