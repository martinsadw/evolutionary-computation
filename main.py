import sys

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, fitness_population
from acs.instance import Instance, print_instance

from utils.misc import  evaluate_population_random, evaluate_population_fixed

from ppa_b.main import prey_predator_algorithm_binary
from ppa_c.main import prey_predator_algorithm_continuous
from pso.main import particle_swarm_optmization
from ga.main import genetic_algorithm
from de.main import differential_evolution

import ppa_b.config
import ppa_c.config
import pso.config
import ga.config
import de.config


def run_method(method_function, fitness_function, instance, config, num_repetitions, **kwargs):
    best_fitness = []
    perf_counter = []
    process_time = []
    cost_value = []

    out_info = {}

    popularity = np.zeros((instance.num_materials,))

    for i in range(num_repetitions):
        np.random.seed(i)
        (population, survival_values) = method_function(instance, config, fitness_function, out_info=out_info, **kwargs)

        best_fitness.append(out_info["best_fitness"])
        perf_counter.append(out_info["perf_counter"])
        process_time.append(out_info["process_time"])

        if len(out_info["cost_value"]) > len(cost_value):
            new_cost_values = out_info["cost_value"][len(cost_value):]
            cost_value.extend(new_cost_values)

        popularity += population[0]

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

    print(cost_value)

    return (cost_value, mean_best_fitness, deviation_best_fitness, mean_perf_counter, mean_process_time)


if __name__ == "__main__":
    instance_config_filename = None
    if (len(sys.argv) >= 2):
        instance_config_filename = sys.argv[1]

    if instance_config_filename is None:
        instance = Instance.load_test()
    else:
        instance = Instance.load_from_file(instance_config_filename)

    config_ppa_b = ppa_b.config.Config.load_from_file("instances/ppa_b_config.txt")
    config_ppa_c = ppa_c.config.Config.load_from_file("instances/ppa_c_config.txt")
    config_pso = pso.config.Config.load_from_file("instances/pso_config.txt")
    config_ga = ga.config.Config.load_from_file("instances/ga_config.txt")
    config_de = de.config.Config.load_from_file("instances/de_config.txt")

    num_repetitions = 1

    results_ppa_b = run_method(prey_predator_algorithm_binary, fitness_population, instance, config_ppa_b, num_repetitions)
    results_ppa_c = run_method(prey_predator_algorithm_continuous, fitness_population, instance, config_ppa_c, num_repetitions, evaluate_function=evaluate_population_random)
    results_pso = run_method(particle_swarm_optmization, fitness, instance, config_pso, num_repetitions, evaluate_function=evaluate_population_random)
    results_ga = run_method(genetic_algorithm, fitness, instance, config_ga, num_repetitions)
    results_de = run_method(differential_evolution, fitness_population, instance, config_de, num_repetitions, evaluate_function=evaluate_population_random)

    fig = plt.figure()
    fig.suptitle('PPAC: best fitness')
    plt.plot(results_ppa_b[0], results_ppa_b[1], label="PPAB")
    plt.plot(results_ppa_c[0], results_ppa_c[1], label="PPAC")
    plt.plot(results_pso[0], results_pso[1], label="PSO")
    plt.plot(results_ga[0], results_ga[1], label="GA")
    plt.plot(results_de[0], results_de[1], label="DE")
    plt.legend(loc=1)
    plt.show()
