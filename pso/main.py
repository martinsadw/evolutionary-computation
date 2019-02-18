import sys
import time

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, fitness_population
from acs.instance import Instance, print_instance

from utils.timer import Timer
from utils.misc import sigmoid, evaluate_population_random, evaluate_population_fixed

from pso.config import Config


cost_counter = 0
def counter_fitness(individual, instance, timer, print_results=False, data=None):
    global cost_counter
    cost_counter += 1
    return fitness(individual, instance, timer, print_results, data=data)


def particle_swarm_optmization(instance, config, fitness_function, evaluate_function, out_info=None):
    num_particles = config.num_particles

    global cost_counter
    cost_counter = 0
    stagnation_counter = 0

    if out_info is not None:
        out_info["best_fitness"] = []
        out_info["perf_counter"] = []
        out_info["process_time"] = []
        out_info["cost_value"] = []

    timer = Timer()

    timer.add_time()
    particle_velocity = np.random.rand(num_particles, instance.num_materials) * (2 * config.max_velocity) - config.max_velocity
    particle_position = evaluate_function(particle_velocity)

    local_best_position = np.copy(particle_position)
    local_best_fitness = np.apply_along_axis(fitness_function, 1, local_best_position, instance, timer)

    global_best_index = np.argmin(local_best_fitness, axis=0)
    global_best_position = np.copy(local_best_position[global_best_index])
    global_best_fitness = local_best_fitness[global_best_index]

    timer.add_time("initialization")

    start_perf_counter = time.perf_counter()
    start_process_time = time.process_time()
    while (stagnation_counter < config.max_stagnation):
        old_global_best_fitness = global_best_fitness

        if out_info is not None:
            out_info["best_fitness"].append(global_best_fitness)
            out_info["perf_counter"].append(time.perf_counter() - start_perf_counter)
            out_info["process_time"].append(time.process_time() - start_process_time)
            out_info["cost_value"].append(cost_counter)

        timer.add_time()
        # TODO(andre:2018-04-18): Atualizar velocidade
        local_influence = np.tile(config.local_influence_parameter * np.random.random(num_particles), (instance.num_materials, 1)).T
        global_influence = np.tile(config.global_influence_parameter * np.random.random(num_particles), (instance.num_materials, 1)).T

        local_distance = local_best_position.astype(int) - particle_position.astype(int)
        global_distance = global_best_position.astype(int) - particle_position.astype(int)

        # print(particle_velocity[0])

        particle_velocity = (config.inertia_parameter * particle_velocity
                             + local_influence * local_distance
                             + global_influence * global_distance)
        particle_velocity = np.clip(particle_velocity, -config.max_velocity, config.max_velocity)
        timer.add_time("update_velocity")

        # Calcula as novas posições
        particle_position = evaluate_function(particle_velocity)
        timer.add_time("update_position")

        # Calcula os novos resultados
        particle_new_fitness = np.apply_along_axis(fitness_function, 1, particle_position, instance, timer)
        timer.add_time("update_fitness")

        # Calcula a mascara de melhores valores para cada particula
        change_mask = (particle_new_fitness < local_best_fitness)

        # Altera o melhor resultado de cada particula
        local_best_position[change_mask] = np.copy(particle_position[change_mask])
        # local_best_position[change_mask] = particle_position[change_mask]
        local_best_fitness[change_mask] = particle_new_fitness[change_mask]

        # Encontra o melhor resultado entre todas as particulas
        global_best_index = np.argmin(local_best_fitness)
        global_best_position = np.copy(local_best_position[global_best_index])
        global_best_fitness = local_best_fitness[global_best_index]

        if global_best_fitness < old_global_best_fitness:
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        timer.add_time("update_best")

    print("Tempo: ")
    print(timer.get_time())
    print("Iterações: ")
    print(timer.get_iterations())
    # print(timer.get_iteration_time())
    print("Tempo total: {}".format(timer.get_total_time()))
    print("Número de iterações: {}".format(len(out_info["cost_value"])))

    if out_info is not None:
        # out_info["best_fitness"].append(survival_values[0])
        out_info["best_fitness"].append(global_best_fitness)
        out_info["perf_counter"].append(time.perf_counter() - start_perf_counter)
        out_info["process_time"].append(time.process_time() - start_process_time)
        out_info["cost_value"].append(cost_counter)

    return (global_best_position, global_best_fitness)


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
        (population, survival_values) = particle_swarm_optmization(instance, config, counter_fitness, evaluate_population_random, out_info=out_info)

        best_fitness.append(out_info["best_fitness"])
        perf_counter.append(out_info["perf_counter"])
        process_time.append(out_info["process_time"])

        if len(out_info["cost_value"]) > len(cost_value):
            new_cost_values = out_info["cost_value"][len(cost_value):]
            cost_value.extend(new_cost_values)

        timer = Timer()
        fitness(population, instance, timer, True)

        popularity += population

        print('#{}\n'.format(i))
        print('Survival values:\n{}\n'.format(survival_values))
        print('Best Individual:\n{}\n'.format(population))
        # array = np.asarray(all_fitness)
        # print('All Fitness:\n{}\n'.format(array))

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
    # fig.suptitle('PSO: perf_counter vs. process_time')
    # plt.plot(mean_perf_counter, 'r.')
    # plt.plot(mean_process_time, 'b.')
    # plt.show()

    fig = plt.figure()
    fig.suptitle('PSO: best fitness')
    plt.plot(cost_value, mean_best_fitness, color='r')
    plt.plot(cost_value, mean_best_fitness+deviation_best_fitness, color='b', linewidth=0.5)
    plt.plot(cost_value, mean_best_fitness-deviation_best_fitness, color='b', linewidth=0.5)
    # plt.errorbar(cost_value, mean_best_fitness, yerr=deviation_best_fitness, color='r', ecolor='b')
    plt.show()

    fig = plt.figure()
    fig.suptitle('PSO: materials selected')
    plt.hist(popularity, bins=10, range=(0, num_repetitions))
    plt.show()

    # np.savetxt("results/all_fitness.csv", all_fitness, fmt="%7.3f", delimiter=",")
