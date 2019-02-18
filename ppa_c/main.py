import sys
import time

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, fitness_population
from acs.instance import Instance, print_instance

from utils.timer import Timer
from utils.roulette import Roulette
from utils.misc import sigmoid, vector_size, random_on_unit_sphere, evaluate_population_random, evaluate_population_fixed, improve_population

from ppa_c.config import Config
from ppa_c.population_movement import move_population_direction, move_population_random, move_population_random_complement, move_population_local_search


cost_counter = 0
def counter_fitness(population, instance, timer, print_results=False):
    global cost_counter
    cost_counter += population.shape[0]
    return fitness_population(population, instance, timer, print_results)


def prey_predator_algorithm_continuous(instance, config, fitness_function, evaluate_function, out_info=None):
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

    population = np.random.rand(population_size, instance.num_materials) * (2 * config.max_position) - config.max_position
    population_best_evaluation = evaluate_function(np.array(population[0:1]))
    population_best_fitness = fitness_function(population_best_evaluation, instance, timer)[0]

    start_perf_counter = time.perf_counter()
    start_process_time = time.process_time()
    while (stagnation_counter < config.max_stagnation):
        timer.add_time()
        population_evaluation = evaluate_function(population)
        survival_values = fitness_function(population_evaluation, instance, timer)

        sorted_indices = np.argsort(survival_values)
        population = population[sorted_indices]
        survival_values = survival_values[sorted_indices]

        if survival_values[0] < population_best_fitness:
            population_best_evaluation = population_evaluation[sorted_indices[0]]
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

        new_population = np.copy(population)

        timer.add_time("creation")

        # Cria as mascaras para separar os diferentes tipos de individuo
        best_prey_mask = np.zeros(population_size, dtype=bool)
        best_prey_mask[0] = True

        predator_mask = np.zeros(population_size, dtype=bool)
        predator_mask[-1] = True

        follow_mask = (np.random.rand(population_size) < config.follow_chance)
        run_mask = ~follow_mask

        follow_mask[best_prey_mask] = False  # Ignora as melhores presas
        follow_mask[predator_mask] = False  # Ignora os predadores

        run_mask[best_prey_mask] = False  # Ignora as melhores presas
        run_mask[predator_mask] = False  # Ignora os predadores

        timer.add_time()

        follow_indices = np.where(follow_mask)[0]
        follow_quant = len(follow_indices)

        tau = 1
        follow_direction = np.empty((follow_quant, instance.num_materials))
        for index in range(follow_quant):
            i = follow_indices[index]
            population_distance = vector_size(population - population[i])
            survival_ratio = survival_values[i] / survival_values

            population_direction = np.exp(survival_ratio ** tau - population_distance * 0.05)[:, np.newaxis] * (population - population[i])
            individual_direction = np.sum(population_direction, axis=0)
            normalized_direction = individual_direction / vector_size(individual_direction)
            follow_direction[index] = normalized_direction

        # Gerar direção multidimensional
        # https://stackoverflow.com/questions/6283080/random-unit-vector-in-multi-dimensional-space

        timer.add_time("follow_calculate_direction")

        # TODO(andre:2018-05-28): Garantir que max_steps nunca é maior do que o numero de materiais
        omega = .5
        predator_distance = survival_values[-1] - survival_values[follow_mask]
        num_steps = config.max_steps * np.random.rand(follow_quant) / np.exp(config.steps_distance_parameter * predator_distance ** omega)
        new_population[follow_mask] = move_population_direction(new_population[follow_mask], num_steps, follow_direction)

        timer.add_time("follow_direction")

        num_steps = np.round(config.min_steps * np.random.rand(follow_quant))
        new_population[follow_mask] = move_population_random(new_population[follow_mask], num_steps)

        timer.add_time("follow_random")

        num_steps = np.round(config.max_steps * np.random.rand(np.count_nonzero(run_mask)))
        new_population[run_mask] = move_population_random_complement(new_population[run_mask], num_steps, population[-1])

        timer.add_time("run")

        new_population[best_prey_mask] = move_population_local_search(new_population[best_prey_mask], fitness_function, evaluate_function, config.min_steps, config.local_search_tries, instance, timer)

        timer.add_time()

        # TODO(andre:2018-12-17): Gerar uma direção dentro de um circulo unitário
        # e multiplicar por max_steps para determinar a direção aleatória
        num_steps = np.round(config.max_steps * np.random.rand(np.count_nonzero(predator_mask)))
        new_population[predator_mask] = move_population_random(new_population[predator_mask], num_steps)

        timer.add_time("predator_random")

        num_steps = np.round(config.min_steps * np.random.rand(np.count_nonzero(predator_mask)))
        worst_prey = np.repeat(population[-2][np.newaxis, :], np.count_nonzero(predator_mask), axis=0)
        new_population[predator_mask] = move_population_direction(new_population[predator_mask], num_steps, worst_prey)

        timer.add_time("predator_follow")

        new_population = np.clip(new_population, -config.max_position, config.max_position)

        population = new_population

    print("Tempo: ")
    print(timer.get_time())
    print("Iterações: ")
    print(timer.get_iterations())
    # print(timer.get_iteration_time())
    print("Tempo total: {}".format(timer.get_total_time()))
    print("Número de iterações: {}".format(len(out_info["cost_value"])))

    population_evaluation = evaluate_function(population)
    survival_values = fitness_function(population_evaluation, instance, timer)
    sorted_indices = np.argsort(survival_values)
    population_evaluation = population_evaluation[sorted_indices]
    survival_values = survival_values[sorted_indices]

    if out_info is not None:
        # out_info["best_fitness"].append(survival_values[0])
        out_info["best_fitness"].append(population_best_fitness)
        out_info["perf_counter"].append(time.perf_counter() - start_perf_counter)
        out_info["process_time"].append(time.process_time() - start_process_time)
        out_info["cost_value"].append(cost_counter)

    return (population_evaluation, survival_values)


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
    best_fitness = []
    perf_counter = []
    process_time = []
    cost_value = []

    out_info = {}

    popularity = np.zeros((instance.num_materials,))

    for i in range(num_repetitions):
        np.random.seed(i)
        (population, survival_values) = prey_predator_algorithm_continuous(instance, config, counter_fitness, evaluate_population_fixed, out_info=out_info)

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
    # fig.suptitle('PPAC: perf_counter vs. process_time')
    # plt.plot(mean_perf_counter, 'r.')
    # plt.plot(mean_process_time, 'b.')
    # plt.show()

    # cost_value = np.arange(num_iterations)

    fig = plt.figure()
    fig.suptitle('PPAC: best fitness')
    plt.plot(cost_value, mean_best_fitness, color='r')
    plt.plot(cost_value, mean_best_fitness+deviation_best_fitness, color='b', linewidth=0.5)
    plt.plot(cost_value, mean_best_fitness-deviation_best_fitness, color='b', linewidth=0.5)
    # plt.errorbar(cost_value, mean_best_fitness, yerr=deviation_best_fitness, color='r', ecolor='b')
    plt.show()

    # fig = plt.figure()
    # fig.suptitle('PPAC: materials selected')
    # plt.hist(popularity, bins=10, range=(0, num_repetitions))
    # plt.show()
