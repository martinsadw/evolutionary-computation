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

from algorithms.ppa_d.config import Config
from algorithms.ppa_d.population_movement import move_population_roulette, move_population_direction, move_population_random, move_population_random_complement, move_population_local_search


def prey_predator_algorithm_discrete(instance, config, fitness_function, out_info=None):
    population_size = config.population_size

    if config.max_steps > instance.num_materials:
        config.max_steps = instance.num_materials

    if config.min_steps > config.max_steps:
        config.min_steps = config.max_steps

    def counter_fitness(individual, instance, student, timer, print_results=False, data=None):
        nonlocal cost_counter
        cost_counter += 1
        return fitness_function(individual, instance, student, timer, print_results, data=data)

    if out_info is not None:
        out_info["best_fitness"] = []
        out_info["partial_fitness"] = []
        out_info["perf_counter"] = []
        out_info["process_time"] = []
        out_info["cost_value"] = []

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

        population = np.random.randint(2, size=(population_size, instance.num_materials), dtype=bool)

        population_best_individual = population[0]
        population_best_fitness = counter_fitness(population[0], instance, student, timer)

        start_perf_counter = time.perf_counter()
        start_process_time = time.process_time()
        while ((not config.cost_budget or cost_counter < config.cost_budget) and
               (not config.num_iterations or iteration_counter < config.num_iterations) and
               (not config.max_stagnation or stagnation_counter < config.max_stagnation)):
            timer.add_time()

            survival_values = np.apply_along_axis(counter_fitness, 1, population, instance, student, timer)
            sorted_indices = np.argsort(survival_values)
            population = population[sorted_indices]
            survival_values = survival_values[sorted_indices]

            iteration_counter += 1
            if survival_values[0] < population_best_fitness:
                population_best_individual = population[0]
                population_best_fitness = survival_values[0]

                stagnation_counter = 0
            else:
                stagnation_counter += 1

            if out_info is not None:
                out_info["best_fitness"][-1].append(population_best_fitness)
                fitness_function(population_best_individual, instance, student, timer, data=out_info["partial_fitness"][-1])
                out_info["perf_counter"][-1].append(time.perf_counter() - start_perf_counter)
                out_info["process_time"][-1].append(time.process_time() - start_process_time)
                out_info["cost_value"][-1].append(cost_counter)

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

            num_steps = np.round(config.min_steps * np.random.rand(follow_quant))
            new_population[follow_mask] = move_population_random(new_population[follow_mask], num_steps)

            timer.add_time("follow_random")

            num_steps = np.round(config.max_steps * np.random.rand(np.count_nonzero(run_mask)))
            new_population[run_mask] = move_population_random_complement(new_population[run_mask], num_steps, population[-1])

            timer.add_time("run")

            new_population[best_prey_mask] = move_population_local_search(new_population[best_prey_mask], counter_fitness, config.min_steps, config.local_search_tries, instance, student, timer)

            timer.add_time()

            num_steps = np.round(config.max_steps * np.random.rand(np.count_nonzero(predator_mask)))
            new_population[predator_mask] = move_population_random(new_population[predator_mask], num_steps)

            timer.add_time("predator_random")

            num_steps = np.round(config.min_steps * np.random.rand(np.count_nonzero(predator_mask)))
            worst_prey = np.repeat(population[-2][np.newaxis, :], np.count_nonzero(predator_mask), axis=0)
            new_population[predator_mask] = move_population_direction(new_population[predator_mask], num_steps, worst_prey)

            timer.add_time("predator_follow")

            population = new_population

        survival_values = np.apply_along_axis(counter_fitness, 1, population, instance, student, timer)
        sorted_indices = np.argsort(survival_values)
        population = population[sorted_indices]
        survival_values = survival_values[sorted_indices]

        if out_info is not None:
            out_info["best_fitness"][-1].append(population_best_fitness)
            fitness_function(population_best_individual, instance, student, timer, data=out_info["partial_fitness"][-1])
            out_info["perf_counter"][-1].append(time.perf_counter() - start_perf_counter)
            out_info["process_time"][-1].append(time.process_time() - start_process_time)
            out_info["cost_value"][-1].append(cost_counter)

        results.append((population_best_individual, population_best_fitness))

    return results
