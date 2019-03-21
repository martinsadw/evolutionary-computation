import sys
import time
import math

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, fitness_population
from acs.instance import Instance, print_instance

from utils.timer import Timer

from de.config import Config


cost_counter = 0
def counter_fitness(population, instance, timer, print_results=False):
    global cost_counter
    cost_counter += population.shape[0]
    return fitness_population(population, instance, timer, print_results)

def differential_evolution(instance, config, fitness_function, out_info=None):
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
    population_best_fitness = fitness_function(population[0], instance, timer)

    start_perf_counter = time.perf_counter()
    start_process_time = time.process_time()
    while (stagnation_counter < config.max_stagnation):
        timer.add_time()
        survival_values = np.apply_along_axis(fitness_function, 1, population, instance, timer)
        sorted_indices = np.argsort(survival_values)
        population = population[sorted_indices]
        survival_values = survival_values[sorted_indices]

        if survival_values[0] < population_best_fitness:
            population_best_fitness = survival_values[0]

            stagnation_counter = 0
        else:
            stagnation_counter += 1

        if out_info is not None:
            out_info["best_fitness"].append(population_best_fitness)
            out_info["perf_counter"].append(time.perf_counter() - start_perf_counter)
            out_info["process_time"].append(time.process_time() - start_process_time)
            out_info["cost_value"].append(cost_counter)
        new_population = np.copy(population)
        #--de
        for p in range(population_size):
            idxs = [idx for idx in range(config.population_size) if idx != p]
            a, b, c = population[np.random.choice(idxs, 3, replace = False)]
            mutant = np.clip(a + config.mutation_chance * (b - c), 0, 1)
            cross_points = np.random.rand(population_size) < config.crossover_rate
            if not np.any(cross_points):
                cross_points[np.random.randint(0, population_size)] = True
            s = np.where(cross_points, mutant, population[p])
            if survival_values[p]>fitness_function(s,instance,timer):
                new_population[p]=np.copy(s)
        #--end de
        population = new_population

    if out_info is not None:
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
        (population, survival_values) = differential_evolution(instance, config, counter_fitness, out_info=out_info)


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

    fig = plt.figure()
    fig.suptitle('DE: best fitness')
    plt.plot(cost_value, mean_best_fitness, color='r')
    plt.plot(cost_value, mean_best_fitness+deviation_best_fitness, color='b', linewidth=0.5)
    plt.plot(cost_value, mean_best_fitness-deviation_best_fitness, color='b', linewidth=0.5)
    plt.show()