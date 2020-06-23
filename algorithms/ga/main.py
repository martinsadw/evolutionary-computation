import sys
import time
import math
import random

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness
from acs.instance import Instance, print_instance

from utils.timer import Timer
from utils.multiobjective import sort_nondominated, crowding_dist

from algorithms.ga.config import Config
from algorithms.ga.copying import copying_gene
from algorithms.ga.local_search import local_search_gene
from algorithms.ga.selection import selection_gene, Selection
from algorithms.ga.crossover import crossover_gene, Crossover
from algorithms.ga.mutation import mutation_gene


def genetic_algorithm(instance, config, fitness_function, out_info=None, verbose=False):
    population_size = config.population_size

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
        if verbose:
            print('[GA] Students progress: %d / %d (%d%%)' % (student + 1, instance.num_learners, (student + 1) * 100 / instance.num_learners))
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

            if survival_values[0] < population_best_fitness:
                population_best_individual = population[0]
                population_best_fitness = survival_values[0]

                stagnation_counter = 0
            else:
                stagnation_counter += 1

            iteration_counter += 1

            if out_info is not None:
                out_info['best_fitness'][-1].append(population_best_fitness)
                fitness_function(population_best_individual, instance, student, timer, data=out_info['partial_fitness'][-1])
                out_info['perf_counter'][-1].append(time.perf_counter() - start_perf_counter)
                out_info['process_time'][-1].append(time.process_time() - start_process_time)
                out_info['cost_value'][-1].append(cost_counter)

            new_population = copying_gene(population, config.copying_method, config)

            if config.use_local_search:
                new_population = local_search_gene(new_population, counter_fitness, config.local_search_method, config)

            remaining_spots = population_size - len(new_population)

            selection_spots = remaining_spots
            if (config.crossover_method == Crossover.THREE_PARENT_CROSSOVER):
                selection_spots = int(3 * math.ceil(remaining_spots / 3.)) * 3
            else:
                selection_spots = int(2 * math.ceil(remaining_spots / 2.))

            parents = selection_gene(population, survival_values, selection_spots, config.selection_method, config)
            children = crossover_gene(parents, config.crossover_method, config)
            mutated = mutation_gene(children, config.mutation_method, config)

            new_population = np.append(new_population, mutated[:remaining_spots], axis=0)
            population = new_population

        if out_info is not None:
            out_info['best_fitness'][-1].append(population_best_fitness)
            fitness_function(population_best_individual, instance, student, timer, data=out_info['partial_fitness'][-1])
            out_info['perf_counter'][-1].append(time.perf_counter() - start_perf_counter)
            out_info['process_time'][-1].append(time.process_time() - start_process_time)
            out_info['cost_value'][-1].append(cost_counter)

        results.append((population_best_individual, population_best_fitness))

    return results
