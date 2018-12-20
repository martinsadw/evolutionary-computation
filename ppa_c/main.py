import sys
import time
import timeit

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, fitness_population
from acs.instance import Instance, print_instance

from utils.timer import Timer
from utils.roulette import Roulette
from utils.misc import sigmoid, vector_size, random_on_unit_sphere

from ppa_c.config import Config
from ppa_c.population_movement import move_population_direction, move_population_random, move_population_random_complement, move_population_local_search

def prey_predator_algorithm_continuous(instance, config, fitness_function, *, best_fitness=None, perf_counter=None, process_time=None):
    population_size = config.population_size

    population = np.random.rand(population_size, instance.num_materials) * (2 * config.max_position) - config.max_position

    timer = Timer()

    start_perf_counter = time.perf_counter()
    start_process_time = time.process_time()
    for iteration in range(config.num_iterations):
        timer.add_time()
        print(vector_size(population).mean())
        print(np.mean(np.sum(np.abs(population), axis=1)))
        print("---------------")
        population_evaluation = evaluate_population(population)
        survival_values = fitness_function(population_evaluation, instance, timer)
        sorted_indices = np.argsort(survival_values)
        population = population[sorted_indices]
        survival_values = survival_values[sorted_indices]

        if best_fitness is not None:
            best_fitness[iteration] = survival_values[0]
        if perf_counter is not None:
            perf_counter[iteration] = time.perf_counter() - start_perf_counter
        if process_time is not None:
            process_time[iteration] = time.process_time() - start_process_time

        new_population = np.copy(population)
        # new_fit=np.copy(population_evaluation)

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

        # print(follow_mask)
        # print(follow_indices)
        # print(survival_values[:, np.newaxis])
        # print(survival_values)
        # print("---------------")

        tau = 1
        follow_direction = np.empty((follow_quant, instance.num_materials))
        for index in range(follow_quant):
            i = follow_indices[index]
            population_distance = vector_size(population - population[i])
            survival_ratio = survival_values / survival_values[i]

            population_direction = np.exp(survival_ratio ** tau - population_distance)[:, np.newaxis] * (population - population[i])
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

        # new_survival_values = fitness_function(new_population, instance, timer)
        # print('Old population:\n{}\n'.format(population))
        # print('New population:\n{}\n'.format(new_population))
        # print('Comparison:\n{}\n'.format(population == new_population))
        # print('Old survival values:\n{}\n'.format(survival_values))
        # print('New survival values:\n{}\n'.format(new_survival_values))

        population = new_population

    print("Tempo: ")
    print(timer.get_time())
    print("Iterações: ")
    print(timer.get_iterations())
    # print(timer.get_iteration_time())
    print("Tempo total: {}".format(timer.get_total_time()))

    population_evaluation = evaluate_population(population)
    survival_values = fitness_function(population_evaluation, instance, timer)
    sorted_indices = np.argsort(survival_values)
    population_evaluation = population_evaluation[sorted_indices]
    survival_values = survival_values[sorted_indices]

    if best_fitness is not None:
        best_fitness[-1] = survival_values[0]
        # best_fitness[-1] = np.mean(survival_values)
        # best_fitness[-1] = survival_values[-1]
    if perf_counter is not None:
        perf_counter[-1] = time.perf_counter() - start_perf_counter
    if process_time is not None:
        process_time[-1] = time.process_time() - start_process_time

    return (population_evaluation, survival_values)


# TODO(andre:2018-12-20): Mover essa função para a utils
def evaluate_population(population):
    population_sigmoid = sigmoid(population)
    population_random = np.random.random(population.shape)
    population_evaluation = (population_sigmoid > population_random).astype(bool)

    return population_evaluation


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

    num_repetitions = 5

    (instance, config) = read_files(instance_config_filename, config_filename)
    # Um valor extra para salvar os valores iniciais
    best_fitness = np.zeros((config.num_iterations + 1, num_repetitions))
    perf_counter = np.zeros((config.num_iterations + 1, num_repetitions))
    process_time = np.zeros((config.num_iterations + 1, num_repetitions))

    for i in range(num_repetitions):
        (population, survival_values) = prey_predator_algorithm_continuous(instance, config, fitness_population, best_fitness=best_fitness[:, i], perf_counter=perf_counter[:, i], process_time=process_time[:, i])
        timer = Timer()
        fitness(population[0], instance, timer, True)
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

    # fig = plt.figure()
    # fig.suptitle('PPA: perf_counter vs. process_time')
    # plt.plot(mean_perf_counter, 'r.')
    # plt.plot(mean_process_time, 'b.')
    # plt.show()

    fig = plt.figure()
    fig.suptitle('PPA: best fitness')
    plt.plot(mean_best_fitness, 'r')
    plt.show()
