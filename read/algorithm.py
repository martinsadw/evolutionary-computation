import os
import pickle

import numpy as np

from acs.objective import multi_fitness, reduce_objectives
from utils.timer import Timer
from read.consts import MAX_OBJECTIVES


def create_results_name_list(instances, algorithms_single, algorithms_multi, num_objectives_list):
    instances_results_name = {}

    for instance in instances:
        instance_list = []

        for algorithm in algorithms_single:
            instance_list.append((algorithm, instance, None))

        for algorithm in algorithms_multi:
            for num_objectives in num_objectives_list:
                instance_list.append((algorithm, instance, num_objectives))

        instances_results_name[instance] = instance_list

    return instances_results_name


def get_results_name(algorithm, instance, num_objectives=None):
    if num_objectives is None:
        name = '%s_%s.pickle' % (algorithm, instance)
    else:
        name = '%s_%d_%s.pickle' % (algorithm, num_objectives, instance)

    return name


def open_results(name, base_folder='results/algorithm_results'):
    file_path = os.path.join(base_folder, name)

    with open(file_path, 'rb') as file:
        file_results = pickle.load(file)

    return file_results


def get_results_info(results):
    return results['info']

def get_results_instance(results):
    return results['info']['instance']

def get_results_data(results):
    return results['data']

# (repetitions, students, individuals, materials)
def get_results_selected_materials(results):
    results_info = get_results_info(results)

    # TODO(andre:2020-07-07): The results for single objetive should return an
    # array with an extra dimension for number of individuals
    population = results['data'][0]
    if results_info['multiobjective'] == False:
        population = population[:, :, np.newaxis, :]

    return population

def get_results_cost(results):
    return results['data'][1]

# (repetitions, students, iterations)
def get_results_best(results):
    # NOTE(andre:2020-09-17): Currently, all results are in the format 'full' and this field is not present
    # if results['info']['format'] != 'full':
    #     raise Exception('List of best results is only present in the "full" format')

    return results['data'][2]

# (repetitions, students, iterations, individuals, objectives)
def get_results_population_fitness(results):
    results_info = get_results_info(results)

    # TODO(andre:2020-07-07): The results for single objetive should return an
    # array with an extra dimension for number of individuals
    population = results['data'][3]
    if results_info['multiobjective'] == False:
        population = population[:, :, :, np.newaxis, :]

    return population

# (repetitions, students, individuals, MAX_OBJECTIVES)
def get_results_best_all_objectives(results):
    results_info = get_results_info(results)
    results_instance = get_results_instance(results)

    # NOTE(andre:2020-09-17): Field 'num_objectives' is only present if 'multiobjective' == True
    if results_info['multiobjective'] == True and results_info['num_objectives'] < MAX_OBJECTIVES:
        results_selected = get_results_selected_materials(results)

        num_repetitions = results_selected.shape[0]
        num_students = results_selected.shape[1]
        num_individuals = results_selected.shape[2]

        # Calculate the fitness value considering all objectives
        timer = Timer()
        population = np.empty((num_repetitions, num_students, num_individuals, MAX_OBJECTIVES))
        for i in range(num_repetitions):
            for j in range(num_students):
                for k in range(num_individuals):
                    population[i, j, k] = multi_fitness(results_selected[i, j, k], results_instance, j, timer)
    else:
        population = get_results_population_fitness(results)[:, :, -1, :, :]

    return population

# (repetitions, students, individuals, num_objectives)
def get_results_best_n_objectives(results, num_objectives):
    results_info = get_results_info(results)
    results_instance = get_results_instance(results)

    # NOTE(andre:2020-09-17): Field 'num_objectives' is only present if 'multiobjective' == True
    if results_info['multiobjective'] == True:
        if results_info['num_objectives'] == num_objectives:
            population = get_results_population_fitness(results)[:, :, -1, :, :]
        elif results_info['num_objectives'] == MAX_OBJECTIVES:
            population = get_results_population_fitness(results)[:, :, -1, :, :]
            population = np.apply_along_axis(reduce_objectives, 3, population, num_objectives)
        else:
            results_selected = get_results_selected_materials(results)

            num_repetitions = results_selected.shape[0]
            num_students = results_selected.shape[1]
            num_individuals = results_selected.shape[2]

            # Calculate the fitness value considering all objectives
            timer = Timer()
            population = np.empty((num_repetitions, num_students, num_individuals, num_objectives))
            for i in range(num_repetitions):
                for j in range(num_students):
                    for k in range(num_individuals):
                        population[i, j, k] = multi_fitness(results_selected[i, j, k], results_instance, j, timer)
            population = reduce_objectives(population, num_objectives)
    else:
        population = get_results_population_fitness(results)[:, :, -1, :, :]
        population = np.apply_along_axis(reduce_objectives, 3, population, num_objectives)

    return population