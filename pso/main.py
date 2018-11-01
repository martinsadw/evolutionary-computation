import sys
import time

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, fitness_population
from acs.instance import Instance, print_instance

from utl.timer import Timer
from utl.misc import sigmoid

from pso.config import Config


def generate_particle_position(particle_velocity):
    particle_sigmoid = sigmoid(particle_velocity)
    particle_random = np.random.random(particle_velocity.shape)
    particle_position = (particle_sigmoid > particle_random).astype(bool)

    return particle_position


def particle_swarm_optmization(instance, config, fitness_function, *, best_fitness=None, perf_counter=None, process_time=None, all_fitness=None):
    num_particles = config.num_particles

    timer = Timer()

    timer.add_time()
    particle_velocity = np.random.rand(
        num_particles, instance.num_materials) * (2 * config.max_velocity) - config.max_velocity
    particle_position = generate_particle_position(particle_velocity)

    local_best_position = np.copy(particle_position)
    local_best_fitness = np.apply_along_axis(
        fitness_function, 1, local_best_position, instance, timer, data=all_fitness)

    global_best_index = np.argmin(local_best_fitness, axis=0)
    global_best_position = np.copy(local_best_position[global_best_index])
    global_best_fitness = local_best_fitness[global_best_index]

    timer.add_time("initialization")

    start_perf_counter = time.perf_counter()
    start_process_time = time.process_time()
    for iteration in range(config.num_iterations):
        if best_fitness is not None:
            best_fitness[iteration] = global_best_fitness
            # best_fitness[iteration] = np.mean(survival_values)
            # best_fitness[iteration] = survival_values[-1]
        if perf_counter is not None:
            perf_counter[iteration] = time.perf_counter() - start_perf_counter
        if process_time is not None:
            process_time[iteration] = time.process_time() - start_process_time

        timer.add_time()
        # TODO(andre:2018-04-18): Atualizar velocidade
        local_influence = np.tile(config.local_influence_parameter *
                                  np.random.random(num_particles), (instance.num_materials, 1)).T
        global_influence = np.tile(config.global_influence_parameter *
                                   np.random.random(num_particles), (instance.num_materials, 1)).T

        local_distance = local_best_position.astype(
            int) - particle_position.astype(int)
        global_distance = global_best_position.astype(
            int) - particle_position.astype(int)

        # print(particle_velocity[0])

        particle_velocity = (config.inertia_parameter * particle_velocity
                             + local_influence * local_distance
                             + global_influence * global_distance)
        particle_velocity = np.clip(
            particle_velocity, -config.max_velocity, config.max_velocity)
        timer.add_time("update_velocity")

        # Calcula as novas posições
        particle_position = generate_particle_position(particle_velocity)
        timer.add_time("update_position")

        # Calcula os novos resultados
        particle_new_fitness = np.apply_along_axis(
            fitness, 1, particle_position, instance, timer, data=all_fitness)
        timer.add_time("update_fitness")

        # Calcula a mascara de melhores valores para cada particula
        change_mask = (particle_new_fitness < local_best_fitness)

        # Altera o melhor resultado de cada particula
        local_best_position[change_mask] = np.copy(
            particle_position[change_mask])
        # local_best_position[change_mask] = particle_position[change_mask]
        local_best_fitness[change_mask] = particle_new_fitness[change_mask]

        # Encontra o melhor resultado entre todas as particulas
        global_best_index = np.argmin(local_best_fitness)
        global_best_position = np.copy(local_best_position[global_best_index])
        global_best_fitness = local_best_fitness[global_best_index]
        timer.add_time("update_best")

    print("Tempo: ")
    print(timer.get_time())
    print("Iterações: ")
    print(timer.get_iterations())
    # print(timer.get_iteration_time())
    print("Tempo total: {}".format(timer.get_total_time()))

    if best_fitness is not None:
        best_fitness[-1] = global_best_fitness
        # best_fitness[iteration] = np.mean(survival_values)
        # best_fitness[iteration] = survival_values[-1]
    if perf_counter is not None:
        perf_counter[-1] = time.perf_counter() - start_perf_counter
    if process_time is not None:
        process_time[-1] = time.process_time() - start_process_time

    # fitness_function(global_best_position, instance, timer, True)

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

    num_repetitions = 100

    (instance, config) = read_files(instance_config_filename, config_filename)
    # Um valor extra para salvar os valores iniciais
    best_fitness = np.zeros((config.num_iterations + 1, num_repetitions))
    perf_counter = np.zeros((config.num_iterations + 1, num_repetitions))
    process_time = np.zeros((config.num_iterations + 1, num_repetitions))
    all_fitness = []

    popularity = np.zeros((instance.num_materials,))

    for i in range(num_repetitions):
        (population, survival_values) = particle_swarm_optmization(instance, config, fitness,
                                                                   best_fitness=best_fitness[:, i], perf_counter=perf_counter[:, i], process_time=process_time[:, i], all_fitness=all_fitness)
        timer = Timer()
        fitness(population, instance, timer, True)
        popularity += population
        print('#{}\n'.format(i))
        print('Survival values:\n{}\n'.format(survival_values))
        print('Best Individual:\n{}\n'.format(population))
        print('Popularity:\n{}\n'.format(popularity))
        # array = np.asarray(all_fitness)
        # print('All Fitness:\n{}\n'.format(array))

    mean_best_fitness = np.mean(best_fitness, axis=1)
    mean_perf_counter = np.mean(perf_counter, axis=1)
    mean_process_time = np.mean(process_time, axis=1)

    print('Statistics:')
    print('Fitness:\n{}\n'.format(mean_best_fitness))
    print('perf_counter:\n{}\n'.format(mean_perf_counter))
    print('process_time:\n{}\n'.format(mean_process_time))

    print('Popularity:\n{}\n'.format(popularity))

    # fig = plt.figure()
    # fig.suptitle('PSO: perf_counter vs. process_time')
    # plt.plot(mean_perf_counter, 'r.')
    # plt.plot(mean_process_time, 'b.')
    # plt.show()

    fig = plt.figure()
    fig.suptitle('PSO: best fitness')
    plt.plot(mean_best_fitness, 'r')
    plt.show()

    fig = plt.figure()
    fig.suptitle('PSO: materials selected')
    plt.hist(popularity, bins=10, range=(0, num_repetitions))
    plt.show()

    # np.savetxt("results/all_fitness.csv", all_fitness, fmt="%7.3f", delimiter=",")
