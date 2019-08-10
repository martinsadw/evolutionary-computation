import sys
import time
import math

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, fitness_population
from acs.instance import Instance

from utils.timer import Timer
from utils.misc import evaluate_population_random, evaluate_population_fixed

from de.config import Config, Evaluator


def differential_evolution(instance, config, fitness_function, out_info=None):
    population_size = config.population_size

    if config.evaluator == Evaluator.FIXED_EVALUATOR:
        evaluate_function = evaluate_population_fixed
    else:
        evaluate_function = evaluate_population_random

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

        # TODO(andre: 2019-04-25): Testar utilizar um valor limite para os valores
        # dos individuos, similar ao PSO e ao PPA_C
        population = np.random.rand(population_size, instance.num_materials) * 2 - 1
        population_evaluation = evaluate_function(population)
        survival_values = np.apply_along_axis(counter_fitness, 1, population_evaluation, instance, student, timer)

        population_best_index = np.argmin(survival_values, axis=0)
        population_best_evaluation = np.copy(population_evaluation[population_best_index])
        population_best_fitness = survival_values[population_best_index]

        start_perf_counter = time.perf_counter()
        start_process_time = time.process_time()
        while ((not config.cost_budget or cost_counter < config.cost_budget) and
               (not config.num_iterations or iteration_counter < config.num_iterations) and
               (not config.max_stagnation or stagnation_counter < config.max_stagnation)):
            timer.add_time()
            old_population_best_fitness = population_best_fitness

            sorted_indices = np.argsort(survival_values)
            population = population[sorted_indices]
            survival_values = survival_values[sorted_indices]

            if out_info is not None:
                out_info["best_fitness"][-1].append(population_best_fitness)
                fitness_function(population_best_evaluation, instance, student, timer, data=out_info["partial_fitness"][-1])
                out_info["perf_counter"][-1].append(time.perf_counter() - start_perf_counter)
                out_info["process_time"][-1].append(time.process_time() - start_process_time)
                out_info["cost_value"][-1].append(cost_counter)

            new_population = np.copy(population)

            #--de
            for p in range(population_size):
                idxs = [idx for idx in range(population_size) if idx != p]
                a, b, c = population[np.random.choice(idxs, 3, replace = False)]

                mutant = np.clip(a + config.mutation_chance * (b - c), 0, 1)

                cross_points = np.random.rand(instance.num_materials) < config.crossover_rate
                if not np.any(cross_points):
                    cross_points[np.random.randint(0, instance.num_materials)] = True

                applicant = np.where(cross_points, mutant, population[p])
                applicant_evaluation = evaluate_function(applicant)
                applicant_fit = counter_fitness(applicant_evaluation, instance, student, timer)

                if applicant_fit < survival_values[p]:
                    new_population[p] = applicant
                    survival_values[p] = applicant_fit

                    if applicant_fit < population_best_fitness:
                        population_best_evaluation = applicant_evaluation
                        population_best_fitness = applicant_fit
            #--end de

            iteration_counter += 1
            if population_best_fitness < old_population_best_fitness:
                stagnation_counter = 0
            else:
                stagnation_counter += 1

            population = new_population

        if out_info is not None:
            out_info["best_fitness"][-1].append(population_best_fitness)
            fitness_function(population_best_evaluation, instance, student, timer, data=out_info["partial_fitness"][-1])
            out_info["perf_counter"][-1].append(time.perf_counter() - start_perf_counter)
            out_info["process_time"][-1].append(time.process_time() - start_process_time)
            out_info["cost_value"][-1].append(cost_counter)

        results.append((population_best_evaluation, population_best_fitness))

    return results


def read_files(instance_config_filename, config_filename):
    if instance_config_filename is None:
        instance = Instance.load_test()
    else:
        instance = Instance.load_from_file(instance_config_filename)

    if config_filename is None:
        config = Config.load_test()
    else:
        config = Config.load_from_file(config_filename)

    return (instance, config)


if __name__ == "__main__":
    instance_config_filename = None
    if (len(sys.argv) >= 2):
        instance_config_filename = sys.argv[1]

    config_filename = None
    if (len(sys.argv) >= 3):
        config_filename = sys.argv[2]

    (instance, config) = read_files(instance_config_filename, config_filename)
    best_fitness = []
    perf_counter = []
    process_time = []
    cost_value = []

    out_info = {}

    # num_repetitions = config.num_repetitions
    num_repetitions = 1

    popularity = np.zeros((instance.num_materials,))

    for i in range(num_repetitions):
        np.random.seed(i)
        (individual, survival_value) = differential_evolution(instance, config, fitness, out_info=out_info)

        best_fitness.append(out_info["best_fitness"])
        perf_counter.append(out_info["perf_counter"])
        process_time.append(out_info["process_time"])

        if len(out_info["cost_value"]) > len(cost_value):
            new_cost_values = out_info["cost_value"][len(cost_value):]
            cost_value.extend(new_cost_values)

        timer = Timer()
        fitness(individual, instance, timer, True)

        popularity += individual

        print('#{}\n'.format(i))
        print('Survival values:\n{}\n'.format(survival_value))
        print('Best Individual:\n{}\n'.format(individual))

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

    fig = plt.figure()
    fig.suptitle('DE: best fitness')
    plt.plot(cost_value, mean_best_fitness, color='r')
    plt.plot(cost_value, mean_best_fitness+deviation_best_fitness, color='b', linewidth=0.5)
    plt.plot(cost_value, mean_best_fitness-deviation_best_fitness, color='b', linewidth=0.5)
    plt.show()
