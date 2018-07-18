import sys
import time

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, fitness_population
from acs.instance import Instance, print_instance

from pso.config import Config


def generate_particle_position(particle_velocity):
    particle_sigmoid = sigmoid(particle_velocity)
    particle_random = np.random.random(particle_velocity.shape)
    particle_position = (particle_sigmoid > particle_random).astype(int)

    return particle_position


def particle_swarm_optmization(instance, config, fitness_function, *, best_fitness=None, perf_counter=None, process_time=None):
    num_particles = config.num_particles

    particle_velocity = np.random.rand(num_particles, instance.num_materials) * (2 * config.max_velocity) - config.max_velocity
    # particle_sigmoid = sigmoid(particle_velocity)
    # particle_random = np.random.random(p_velocity.shape)
    # p_position = (p_sigmoid > p_random).astype(int)
    particle_position = generate_particle_position(particle_velocity)

    local_best_position = np.copy(p_position)
    local_best_result = np.apply_along_axis(fitness, 1, local_best_position)

    global_best_index = np.argmin(local_best_result, axis=0)
    global_best_position = local_best_position[global_best_index]
    global_best_result = local_best_result[global_best_index]

    # print(local_best_position)
    # print(local_best_result)
    # print(global_best_position)
    # print(global_best_result)

    for i in range(num_iterations):
        # TODO(andre:2018-04-18): Atualizar velocidade
        p_influence = np.tile(config.local_influence_parameter * np.random.random(num_particles), (instance.num_materials, 1)).T
        g_influence = np.tile(config.global_influence_parameter * np.random.random(num_particles), (instance.num_materials, 1)).T

        p_velocity = param_a * p_velocity + p_influence * (p_best_position - p_position) + g_influence * (g_best_position - p_position)
        p_velocity = np.clip(p_velocity, -config.max_velocity, config.max_velocity)

        # Calcula as novas posições
        p_new_sigmoid = sigmoid(p_velocity)
        p_new_random = np.random.random(p_velocity.shape)
        p_position = (p_new_sigmoid > p_new_random).astype(int)

        # Calcula os novos resultados
        p_new_result = np.apply_along_axis(fitness, 1, p_position)

        # Calcula a mascara de melhores valores para cada particula
        change_mask = (p_new_result < p_best_result)

        # Altera o melhor resultado de cada particula
        p_best_result[change_mask] = p_new_result[change_mask]
        p_best_position[change_mask] = p_position[change_mask]

        # Encontra o melhor resultado entre todas as particulas
        g_best_index = np.argmin(p_best_result, axis=0)
        g_best_position = p_best_position[g_best_index]
        g_best_result = p_best_result[g_best_index]

    # print(p_best_position)
    # print(p_best_result)
    # print(g_best_position)
    # print(g_best_result)

    x = get_float(g_best_position[16:32], 10)
    y = get_float(g_best_position[0:16], 10)
    print("Melhor resultado: (" + str(x) + ", " + str(y) + ") -> " + str(g_best_result))


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
        (population, survival_values) = particle_swarm_optmization(instance, config, fitness_population, best_fitness=best_fitness[:,i], perf_counter=perf_counter[:,i], process_time=process_time[:,i])
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
