import sys
import time
import timeit

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, fitness_population
from acs.instance import Instance, print_instance

from utils.timer import Timer
from utils.roulette import Roulette
from utils.misc import hamming_distance

from ppa_b.config import Config
from ppa_b.population_movement import move_population_roulette, move_population_direction, move_population_random, move_population_random_complement, move_population_local_search


cost_counter = 0
def counter_fitness(population, instance, timer, print_results=False):
    global cost_counter
    cost_counter += population.shape[0]
    return fitness_population(population, instance, timer, print_results)


def prey_predator_algorithm_binary(instance, config, fitness_function, out_info=None):
    population_size = config.population_size

    global cost_counter
    cost_counter = 0
    stagnation_counter = 0

    # Um valor extra para salvar os valores iniciais
    if out_info is not None:
        out_info["best_fitness"] = []
        out_info["perf_counter"] = []
        out_info["process_time"] = []
        out_info["cost_value"] = []

    timer = Timer()

    population = np.random.randint(2, size=(population_size, instance.num_materials), dtype=bool)
    population_best_individual = population[0]
    population_best_fitness = fitness_function(population[0:1], instance, timer)[0]

    start_perf_counter = time.perf_counter()
    start_process_time = time.process_time()
    while (stagnation_counter < config.max_stagnation):
        timer.add_time()
        # print('==========================' + str(iteration))
        survival_values = fitness_function(population, instance, timer)
        sorted_indices = np.argsort(survival_values)
        population = population[sorted_indices]
        survival_values = survival_values[sorted_indices]
        # print('Survival values:\n{}\n'.format(survival_values))

        if survival_values[0] < population_best_fitness:
            population_best_individual = population[0]
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

        # print('Best prey mask: {}'.format(best_prey_mask))
        # print(' Predator mask: {}'.format(predator_mask))
        # print('   Follow mask: {}'.format(follow_mask))
        # print('      Run mask: {}'.format(run_mask))

        timer.add_time()

        follow_indices = np.where(follow_mask)[0]
        follow_quant = len(follow_indices)

        population_distance = [[hamming_distance(population[j], population[i]) / instance.num_materials for j in range(i)] for i in follow_indices]
        survival_ratio = [[survival_values[j] / survival_values[i] for j in range(i)] for i in follow_indices]
        follow_chance = [[(2 - config.follow_distance_parameter * population_distance[i][j] - config.follow_survival_parameter * survival_ratio[i][j]) / 2 for j in range(follow_indices[i])] for i in range(follow_quant)]
        roulette_array = np.array([Roulette(follow_chance[i]) for i in range(follow_quant)])

        timer.add_time("follow_chance")

        # TODO(andre:2018-05-28): Garantir que max_steps nunca é maior do que o numero de materiais
        # TODO(andre:2018-12-20): Verificar o calculo do número de passos. Ele está usando a distância até a proxima presa e não a distância até o predador
        num_steps = np.round(config.max_steps * np.random.rand(follow_quant) / np.exp(config.steps_distance_parameter * np.array([i[-1] for i in population_distance])))
        new_population[follow_mask] = move_population_roulette(new_population[follow_mask], num_steps, roulette_array, population)

        timer.add_time("follow_roulette")

        # num_steps = np.round(config.min_steps * np.random.rand(population_size))
        # new_population = move_population_random(new_population, num_steps, follow_mask)
        num_steps = np.round(config.min_steps * np.random.rand(follow_quant))
        new_population[follow_mask] = move_population_random(new_population[follow_mask], num_steps)

        timer.add_time("follow_random")

        # num_steps = np.round(config.max_steps * np.random.rand(population_size))
        # new_population = move_population_random_complement(new_population, num_steps, population[-1], run_mask)
        num_steps = np.round(config.max_steps * np.random.rand(np.count_nonzero(run_mask)))
        new_population[run_mask] = move_population_random_complement(new_population[run_mask], num_steps, population[-1])

        timer.add_time("run")

        new_population[best_prey_mask] = move_population_local_search(new_population[best_prey_mask], fitness_function, config.min_steps, config.local_search_tries, instance, timer)

        timer.add_time()

        # num_steps = np.round(config.max_steps * np.random.rand(population_size))
        # new_population = move_population_random(new_population, num_steps, predator_mask)
        num_steps = np.round(config.max_steps * np.random.rand(np.count_nonzero(predator_mask)))
        new_population[predator_mask] = move_population_random(new_population[predator_mask], num_steps)

        timer.add_time("predator_random")

        # num_steps = np.round(config.min_steps * np.random.rand(population_size))
        # worst_prey = np.repeat(population[-2][np.newaxis, :], population_size, axis=0)
        # new_population = move_population_direction(new_population, num_steps, worst_prey, predator_mask)
        num_steps = np.round(config.min_steps * np.random.rand(np.count_nonzero(predator_mask)))
        worst_prey = np.repeat(population[-2][np.newaxis, :], np.count_nonzero(predator_mask), axis=0)
        new_population[predator_mask] = move_population_direction(new_population[predator_mask], num_steps, worst_prey)

        timer.add_time("predator_follow")

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
    print("Número de iterações: {}".format(len(out_info["cost_value"])))

    survival_values = fitness_function(population, instance, timer)
    sorted_indices = np.argsort(survival_values)
    population = population[sorted_indices]
    survival_values = survival_values[sorted_indices]

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
        (population, survival_values) = prey_predator_algorithm_binary(instance, config, counter_fitness, out_info=out_info)

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
    fig.suptitle('PPA: best fitness')
    plt.plot(cost_value, mean_best_fitness, color='r')
    plt.plot(cost_value, mean_best_fitness+deviation_best_fitness, color='b', linewidth=0.5)
    plt.plot(cost_value, mean_best_fitness-deviation_best_fitness, color='b', linewidth=0.5)
    # plt.errorbar(cost_value, mean_best_fitness, yerr=deviation_best_fitness, color='r', ecolor='b')
    plt.show()

    fig = plt.figure()
    fig.suptitle('PPA: materials selected')
    plt.hist(popularity, bins=10, range=(0, num_repetitions))
    plt.show()

    # timeit_globals = {
    #     'prey_predator_algorithm_binary': prey_predator_algorithm_binary,
    #     'instance': instance,
    #     'config': config,
    #     'fitness_population': fitness_population
    # }
    # a = timeit.Timer('prey_predator_algorithm_binary(instance, config, fitness_population)', globals=timeit_globals).repeat(10, 1)
    # b = np.array(a)
    # print('Media: ' + str(np.mean(b)))
    # print('Min: ' + str(np.min(b)))
    # print('Max: ' + str(np.max(b)))

    # np.savetxt("results/fitness_100_30.csv", best_fitness, fmt="%7.3f", delimiter=",")
    # np.savetxt("results/time_100_30.csv", process_time, fmt="%8.3f", delimiter=",")

    # instance_test = Instance.load_from_file(config_filename)
    # print('a: {}\n'.format(fitness(np.array([True, False, False, False, False, False]), instance_test, True)))
    # print('b: {}\n'.format(fitness(np.array([False, False, False, False, True, False]), instance_test, True)))
    # print('c: {}\n'.format(fitness(np.array([True, True, True, True, True, True]), instance_test, True)))
    # print('d: {}\n'.format(fitness(np.array([False, False, False, False, False, False]), instance_test, True)))
