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

from algorithms.nsga_ii.config import Config

from algorithms.ga.local_search import local_search_gene
from algorithms.ga.selection import selection_gene, Selection
from algorithms.ga.crossover import crossover_gene, Crossover
from algorithms.ga.mutation import mutation_gene


def nsga_ii(instance, config, fitness_function, out_info=None, **kwargs):
    population_size = config.population_size

    def counter_fitness(individual, instance, student, timer, print_results=False, data=None, **kwargs):
        nonlocal cost_counter
        cost_counter += 1
        return fitness_function(individual, instance, student, timer, print_results, data=data, **kwargs)

    if out_info is not None:
        out_info['best_fitness'] = []
        out_info['partial_fitness'] = []
        out_info['perf_counter'] = []
        out_info['process_time'] = []
        out_info['cost_value'] = []

    results = []

    for student in range(instance.num_learners):
        print('\n\n\n\n---------------------------------------------\n\n\n\nNew Student')
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
        population_best_fitness = np.array(counter_fitness(population[0], instance, student, timer, **kwargs))

        survival_values = np.apply_along_axis(counter_fitness, 1, population, instance, student, timer, **kwargs)
        sorted_fronts = sort_nondominated(survival_values, sign=-1)

        distance = np.zeros((survival_values.shape[0],))
        for front in sorted_fronts:
            distance[front] = crowding_dist(survival_values[front])

        start_perf_counter = time.perf_counter()
        start_process_time = time.process_time()
        while ((not config.cost_budget or cost_counter < config.cost_budget) and
               (not config.num_iterations or iteration_counter < config.num_iterations) and
               (not config.max_stagnation or stagnation_counter < config.max_stagnation)):
            timer.add_time()

            iteration_counter += 1

            if out_info is not None:
                out_info['best_fitness'][-1].append(population_best_fitness)
                fitness_function(population_best_individual, instance, student, timer, data=out_info['partial_fitness'][-1], **kwargs)
                out_info['perf_counter'][-1].append(time.perf_counter() - start_perf_counter)
                out_info['process_time'][-1].append(time.process_time() - start_process_time)
                out_info['cost_value'][-1].append(cost_counter)

            remaining_spots = population_size

            selection_spots = remaining_spots
            if (config.crossover_method == Crossover.THREE_PARENT_CROSSOVER):
                selection_spots = int(3 * math.ceil(remaining_spots / 3.)) * 3
            else:
                selection_spots = int(2 * math.ceil(remaining_spots / 2.))

            # print(population.shape)
            # print(survival_values.shape)
            # print(selection_spots)

            parents = selection_gene(population, survival_values, selection_spots, Selection.NSGA_II_SELECTION, config, crowding_dist=distance)
            children = crossover_gene(parents, config.crossover_method, config)
            mutated = mutation_gene(children, config.mutation_method, config)
            mutated = mutated[:remaining_spots]

            # Calculates the survival value of only the new individuals
            new_survival_values = np.apply_along_axis(counter_fitness, 1, mutated, instance, student, timer, **kwargs)

            new_population = np.append(population, mutated, axis=0)
            new_survival_values = np.append(survival_values, new_survival_values, axis=0)

            print('----------------------')
            sorted_fronts = sort_nondominated(new_survival_values, sign=-1)

            new_distance = np.zeros((new_survival_values.shape[0],))
            sorted_indices = []
            for front in sorted_fronts:
                front_distance = crowding_dist(new_survival_values[front])
                sorted_indices.extend([x for (_, x) in sorted(zip(front_distance, front), reverse=True)])
                new_distance[front] = front_distance

            new_population = new_population[sorted_indices]
            new_survival_values = new_survival_values[sorted_indices]
            new_distance = new_distance[sorted_indices]

            population = new_population[:population_size]
            survival_values = new_survival_values[:population_size]
            distance = new_distance[:population_size]

            res = np.sum(survival_values, axis=1)
            print(np.min(res))

        if out_info is not None:
            out_info['best_fitness'][-1].append(population_best_fitness)
            fitness_function(population_best_individual, instance, student, timer, data=out_info['partial_fitness'][-1], **kwargs)
            out_info['perf_counter'][-1].append(time.perf_counter() - start_perf_counter)
            out_info['process_time'][-1].append(time.process_time() - start_process_time)
            out_info['cost_value'][-1].append(cost_counter)

        results.append((population_best_individual, population_best_fitness))

    return results
