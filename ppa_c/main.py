import sys
import time
import timeit
from collections import defaultdict
from statistics import mean, pstdev

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, fitness_population
from acs.instance import Instance, print_instance

from utils.timer import Timer
from utils.roulette import Roulette
from utils.misc import sigmoid, vector_size, random_on_unit_sphere, evaluate_population, improve_population

from ppa_c.config import Config
from ppa_c.population_movement import move_population_direction, move_population_random, move_population_random_complement, move_population_local_search


cost_counter = 0
def counter_fitness(population, instance, timer, print_results=False):
    global cost_counter
    cost_counter += population.shape[0]
    return fitness_population(population, instance, timer, print_results)


def prey_predator_algorithm_continuous(instance, config, fitness_function, *, out_info=None):
    population_size = config.population_size

    global cost_counter
    cost_counter = 0
    stagnation_counter = 0

    # Um valor extra para salvar os valores iniciais
    if out_info is not None:
        # out_info["best_fitness"] = np.zeros((config.num_iterations + 1,))
        # out_info["cost_value"] = np.zeros((config.num_iterations + 1,))
        # out_info["perf_counter"] = np.zeros((config.num_iterations + 1,))
        # out_info["process_time"] = np.zeros((config.num_iterations + 1,))
        out_info["best_fitness"] = {}
        out_info["perf_counter"] = {}
        out_info["process_time"] = {}

    timer = Timer()

    population = np.random.rand(population_size, instance.num_materials) * (2 * config.max_position) - config.max_position
    population_best_evaluation = evaluate_population(np.array(population[0:1]))
    population_best_fitness = fitness_function(population_best_evaluation, instance, timer)[0]

    start_perf_counter = time.perf_counter()
    start_process_time = time.process_time()
    while (stagnation_counter < config.max_stagnation):
        timer.add_time()
        population_evaluation = evaluate_population(population)
        survival_values = fitness_function(population_evaluation, instance, timer)

        sorted_indices = np.argsort(survival_values)
        population = population[sorted_indices]
        survival_values = survival_values[sorted_indices]

        if survival_values[sorted_indices[0]] < population_best_fitness:
            population_best_evaluation = population_evaluation[sorted_indices[0]]
            population_best_fitness = survival_values[sorted_indices[0]]

            stagnation_counter = 0
        else:
            stagnation_counter += 1

        if out_info is not None:
            # out_info["best_fitness"].append(survival_values[0])
            out_info["best_fitness"][cost_counter] = population_best_fitness.min()
            out_info["perf_counter"][cost_counter] = time.perf_counter() - start_perf_counter
            out_info["process_time"][cost_counter] = time.process_time() - start_process_time

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

        new_population[best_prey_mask] = move_population_local_search(new_population[best_prey_mask], fitness_function, config.min_steps, config.local_search_tries, instance, timer)

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

    population_evaluation = evaluate_population(population)
    survival_values = fitness_function(population_evaluation, instance, timer, True)
    sorted_indices = np.argsort(survival_values)
    population_evaluation = population_evaluation[sorted_indices]
    survival_values = survival_values[sorted_indices]

    if out_info is not None:
        # out_info["best_fitness"].append(survival_values[0])
        out_info["best_fitness"][cost_counter] = population_best_fitness.min()
        out_info["perf_counter"][cost_counter] = time.perf_counter() - start_perf_counter
        out_info["process_time"][cost_counter] = time.process_time() - start_process_time

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

    num_repetitions = 20

    (instance, config) = read_files(instance_config_filename, config_filename)
    best_fitness = defaultdict(list)
    perf_counter = defaultdict(list)
    process_time = defaultdict(list)

    out_info = {}

    for i in range(num_repetitions):
        np.random.seed(i)
        # (population, survival_values) = prey_predator_algorithm_continuous(instance, config, fitness_population, best_fitness=best_fitness[:, i], perf_counter=perf_counter[:, i], process_time=process_time[:, i])
        (population, survival_values) = prey_predator_algorithm_continuous(instance, config, counter_fitness, out_info=out_info)

        for key in out_info["best_fitness"].keys():
            best_fitness[key].append(out_info["best_fitness"][key])
            perf_counter[key].append(out_info["perf_counter"][key])
            process_time[key].append(out_info["process_time"][key])

        timer = Timer()
        fitness(population[0], instance, timer, True)

        print('#{}\n'.format(i))
        print('Survival values:\n{}\n'.format(survival_values))
        print('Best Individual:\n{}\n'.format(population[0]))

    num_iterations = len(best_fitness.keys())

    cost_value = np.empty(num_iterations)
    mean_best_fitness = np.empty(num_iterations)
    deviation_best_fitness = np.empty(num_iterations)
    mean_perf_counter = np.empty(num_iterations)
    mean_process_time = np.empty(num_iterations)

    sorted_keys = sorted(best_fitness.keys())
    for iteration in range(num_iterations):
        key = sorted_keys[iteration]

        cost_value[iteration] = key
        mean_best_fitness[iteration] = mean(best_fitness[key])
        deviation_best_fitness[iteration] = pstdev(best_fitness[key], mean_best_fitness[iteration])
        mean_perf_counter[iteration] = mean(perf_counter[key])
        mean_process_time[iteration] = mean(process_time[key])

    print('Statistics:')
    print('Fitness:\n{}\n'.format(mean_best_fitness))
    print('perf_counter:\n{}\n'.format(mean_perf_counter))
    print('process_time:\n{}\n'.format(mean_process_time))

    # fig = plt.figure()
    # fig.suptitle('PPA: perf_counter vs. process_time')
    # plt.plot(mean_perf_counter, 'r.')
    # plt.plot(mean_process_time, 'b.')
    # plt.show()

    # cost_value = np.arange(num_iterations)

    fig = plt.figure()
    fig.suptitle('PPA: best fitness')
    plt.plot(cost_value, mean_best_fitness, color='r')
    plt.plot(cost_value, mean_best_fitness+deviation_best_fitness, color='b', linewidth=0.5)
    plt.plot(cost_value, mean_best_fitness-deviation_best_fitness, color='b', linewidth=0.5)
    # plt.errorbar(cost_value, mean_best_fitness, yerr=deviation_best_fitness, color='r', ecolor='b')
    plt.show()
