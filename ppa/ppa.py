import sys
import time

import numpy as np
import matplotlib.pyplot as plt

from objective import fitness, fitness_population
from config import Config
from instance import Instance, print_instance
from roulette import Roulette
from population_movement import move_population_roulette, move_population_direction, move_population_random, move_population_random_complement, move_population_local_search
from utils import hamming_distance


def prey_predator_algorithm(instance, config, *, best_fitness, perf_counter, process_time):
    population_size = config.population_size

    population = np.random.randint(2, size=(population_size, instance.num_materials), dtype=bool)

    start_perf_counter = time.perf_counter()
    start_process_time = time.process_time()
    for iteration in range(config.num_iterations):
        # print('==========================' + str(iteration))
        survival_values = fitness_population(population, instance)
        sorted_indices = np.argsort(survival_values)
        population = population[sorted_indices]
        survival_values = survival_values[sorted_indices]
        # print('Survival values:\n{}\n'.format(survival_values))

        if best_fitness is not None:
            best_fitness[iteration] = survival_values[0]
        if perf_counter is not None:
            perf_counter[iteration] = time.perf_counter() - start_perf_counter
        if process_time is not None:
            process_time[iteration] = time.process_time() - start_process_time

        new_population = np.copy(population)

        population_distance = np.empty((population_size, population_size))
        survival_ratio = np.empty((population_size, population_size))
        for i in range(population_size):
            for j in range(population_size):
                population_distance[i, j] = hamming_distance(population[j], population[i]) / instance.num_materials
                survival_ratio[i, j] = survival_values[j] / survival_values[i]
        follow_chance = (2 - config.follow_distance_parameter * population_distance - config.follow_survival_parameter * survival_ratio) / 2
        roulette_array = np.array([Roulette(follow_chance[i, :i].tolist()) for i in range(population_size)])

        # Cria as mascaras para separar os diferentes tipos de individuo
        best_prey_mask = np.zeros(population_size, dtype=bool)
        best_prey_mask[0] = True

        predator_mask = np.zeros(population_size, dtype=bool)
        predator_mask[-1] = True

        follow_mask = (np.random.rand(population_size) < config.follow_chance)
        run_mask = ~follow_mask

        follow_mask[best_prey_mask] = False # Ignora as melhores presas
        follow_mask[predator_mask] = False # Ignora os predadores

        run_mask[best_prey_mask] = False # Ignora as melhores presas
        run_mask[predator_mask] = False # Ignora os predadores

        # print('Best prey mask: {}'.format(best_prey_mask))
        # print(' Predator mask: {}'.format(predator_mask))
        # print('   Follow mask: {}'.format(follow_mask))
        # print('      Run mask: {}'.format(run_mask))

        # TODO(andre:2018-05-28): Garantir que max_steps nunca é maior do que o numero de materiais
        num_steps = np.round(config.max_steps * np.random.rand(population_size) / np.exp(config.steps_distance_parameter * population_distance[:, -1]))
        new_population = move_population_roulette(new_population, num_steps, roulette_array, population, follow_mask)

        num_steps = np.round(config.min_steps * np.random.rand(population_size))
        new_population = move_population_random(new_population, num_steps, follow_mask)

        num_steps = np.round(config.max_steps * np.random.rand(population_size))
        new_population = move_population_random_complement(new_population, num_steps, population[-1], run_mask)

        new_population = move_population_local_search(new_population, best_prey_mask, config.min_steps, config.local_search_tries, instance)

        num_steps = np.round(config.max_steps * np.random.rand(population_size))
        new_population = move_population_random(new_population, num_steps, predator_mask)

        num_steps = np.round(config.min_steps * np.random.rand(population_size))
        worst_prey = np.repeat(population[-2][np.newaxis, :], population_size, axis=0)
        new_population = move_population_direction(new_population, num_steps, worst_prey, predator_mask)

        new_survival_values = fitness_population(new_population, instance)
        # print('Old population:\n{}\n'.format(population))
        # print('New population:\n{}\n'.format(new_population))
        # print('Comparison:\n{}\n'.format(population == new_population))
        # print('Old survival values:\n{}\n'.format(survival_values))
        # print('New survival values:\n{}\n'.format(new_survival_values))

        population = new_population

    survival_values = fitness_population(population, instance)
    sorted_indices = np.argsort(survival_values)
    population = population[sorted_indices]
    survival_values = survival_values[sorted_indices]

    if best_fitness is not None:
        best_fitness[-1] = survival_values[0]
    if perf_counter is not None:
        perf_counter[-1] = time.perf_counter() - start_perf_counter
    if process_time is not None:
        process_time[-1] = time.process_time() - start_process_time

    return (population, survival_values)


def read_files(instance_config_filename, config_filename):
    if instance_config_filename is None:
        instance = Instance.load_test()
    else:
        instance = Instance.load_from_file(instance_config_filename)

    # print_instance(instance)
    # print("")

    if config_filename is None:
        config = Config.load_test()
    else:
        config = Config.load_from_file(config_filename)

    return (instance, config)


if __name__ == "__main__":
    # assert(len(sys.argv) >= 2)
    instance_config_filename = None
    if (len(sys.argv) >= 2):
        instance_config_filename = sys.argv[1]

    config_filename = None
    if (len(sys.argv) >= 3):
        config_filename = sys.argv[2]

    num_repetitions = 10

    (instance, config) = read_files(instance_config_filename, config_filename)
    best_fitness = np.zeros((config.num_iterations + 1, num_repetitions)) # Um valor extra para salvar os valores iniciais
    perf_counter = np.zeros((config.num_iterations + 1, num_repetitions))
    process_time = np.zeros((config.num_iterations + 1, num_repetitions))

    for i in range(num_repetitions):
        (population, survival_values) = prey_predator_algorithm(instance, config, best_fitness=best_fitness[:,i], perf_counter=perf_counter[:,i], process_time=process_time[:,i])
        print('#{}\n'.format(i))
        print('Survival values:\n{}\n'.format(survival_values))
        print('Best Individual:\n{}\n'.format(population[0]))

    mean_best_fitness = np.mean(best_fitness, axis=1)
    mean_perf_counter = np.mean(perf_counter, axis=1)
    mean_process_time = np.mean(process_time, axis=1)

    print('Statistics:')
    print('Fitness:\n{}\n'.format(mean_best_fitness))
    print('perf_counter:\n{}\n'.format(mean_perf_counter))
    print('process_time:\n{}\n'.format(mean_process_time))

    fig = plt.figure()
    fig.suptitle('PPA: perf_counter vs. process_time')
    plt.plot(mean_perf_counter, 'r.')
    plt.plot(mean_process_time, 'b.')
    plt.show()

    fig = plt.figure()
    fig.suptitle('PPA: best fitness')
    plt.plot(mean_best_fitness, 'r')
    plt.show()

    # instance_test = Instance.load_from_file(config_filename)
    # print('a: {}\n'.format(fitness(np.array([True, False, False, False, False, False]), instance_test, True)))
    # print('b: {}\n'.format(fitness(np.array([False, False, False, False, True, False]), instance_test, True)))
    # print('c: {}\n'.format(fitness(np.array([True, True, True, True, True, True]), instance_test, True)))
    # print('d: {}\n'.format(fitness(np.array([False, False, False, False, False, False]), instance_test, True)))
