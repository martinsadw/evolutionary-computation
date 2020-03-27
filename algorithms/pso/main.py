import sys
import time

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, fitness_population
from acs.instance import Instance, print_instance

from utils.timer import Timer
from utils.misc import sigmoid, evaluate_population_random, evaluate_population_fixed

from algorithms.pso.config import Config, Evaluator


def particle_swarm_optmization(instance, config, fitness_function, out_info=None):
    num_particles = config.num_particles

    if config.evaluator == Evaluator.FIXED_EVALUATOR:
        evaluate_function = evaluate_population_fixed
    else:
        evaluate_function = evaluate_population_random

    def counter_fitness(individual, instance, student, timer, print_results=False, data=None):
        nonlocal cost_counter
        cost_counter += 1
        return fitness_function(individual, instance, student, timer, print_results, data=data)

    if out_info is not None:
        out_info['best_fitness'] = []
        out_info['partial_fitness'] = []
        out_info['perf_counter'] = []
        out_info['process_time'] = []
        out_info['cost_value'] = []

    results = []

    for student in range(instance.num_learners):
        cost_counter = 0
        iteration_counter = 0
        stagnation_counter = 0

        if out_info is not None:
            out_info['best_fitness'].append([])
            out_info['partial_fitness'].append([])
            out_info['perf_counter'].append([])
            out_info['process_time'].append([])
            out_info['cost_value'].append([])

        timer = Timer()

        timer.add_time()
        particle_velocity = np.random.rand(num_particles, instance.num_materials) * (2 * config.max_velocity) - config.max_velocity
        particle_position = evaluate_function(particle_velocity)

        local_best_position = np.copy(particle_position)
        local_best_fitness = np.apply_along_axis(counter_fitness, 1, local_best_position, instance, student, timer)

        global_best_index = np.argmin(local_best_fitness, axis=0)
        global_best_position = np.copy(local_best_position[global_best_index])
        global_best_fitness = local_best_fitness[global_best_index]

        timer.add_time("initialization")

        start_perf_counter = time.perf_counter()
        start_process_time = time.process_time()
        while ((not config.cost_budget or cost_counter < config.cost_budget) and
               (not config.num_iterations or iteration_counter < config.num_iterations) and
               (not config.max_stagnation or stagnation_counter < config.max_stagnation)):
            old_global_best_fitness = global_best_fitness

            if out_info is not None:
                out_info["best_fitness"][-1].append(global_best_fitness)
                fitness_function(global_best_position, instance, student, timer, data=out_info["partial_fitness"][-1])
                out_info["perf_counter"][-1].append(time.perf_counter() - start_perf_counter)
                out_info["process_time"][-1].append(time.process_time() - start_process_time)
                out_info["cost_value"][-1].append(cost_counter)

            timer.add_time()
            local_influence = np.tile(config.local_influence_parameter * np.random.random(num_particles), (instance.num_materials, 1)).T
            global_influence = np.tile(config.global_influence_parameter * np.random.random(num_particles), (instance.num_materials, 1)).T

            local_distance = local_best_position.astype(int) - particle_position.astype(int)
            global_distance = global_best_position.astype(int) - particle_position.astype(int)

            particle_velocity = (config.inertia_parameter * particle_velocity
                                 + local_influence * local_distance
                                 + global_influence * global_distance)
            particle_velocity = np.clip(particle_velocity, -config.max_velocity, config.max_velocity)
            timer.add_time("update_velocity")

            # Calcula as novas posições
            particle_position = evaluate_function(particle_velocity)
            timer.add_time("update_position")

            # Calcula os novos resultados
            particle_new_fitness = np.apply_along_axis(counter_fitness, 1, particle_position, instance, student, timer)
            timer.add_time("update_fitness")

            # Calcula a mascara de melhores valores para cada particula
            change_mask = (particle_new_fitness < local_best_fitness)

            # Altera o melhor resultado de cada particula
            local_best_position[change_mask] = np.copy(particle_position[change_mask])
            local_best_fitness[change_mask] = particle_new_fitness[change_mask]

            # Encontra o melhor resultado entre todas as particulas
            global_best_index = np.argmin(local_best_fitness)
            global_best_position = np.copy(local_best_position[global_best_index])
            global_best_fitness = local_best_fitness[global_best_index]

            iteration_counter += 1
            if global_best_fitness < old_global_best_fitness:
                stagnation_counter = 0
            else:
                stagnation_counter += 1

            timer.add_time("update_best")

        if out_info is not None:
            out_info["best_fitness"][-1].append(global_best_fitness)
            fitness_function(global_best_position, instance, student, timer, data=out_info["partial_fitness"][-1])
            out_info["perf_counter"][-1].append(time.perf_counter() - start_perf_counter)
            out_info["process_time"][-1].append(time.process_time() - start_process_time)
            out_info["cost_value"][-1].append(cost_counter)

        results.append((global_best_position, global_best_fitness))

    return results
