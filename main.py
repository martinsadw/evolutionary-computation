import sys

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, fitness_population
from acs.instance import Instance, print_instance

from utils.misc import evaluate_population_fixed, evaluate_population_random
from utils.runner import run_method

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


# TODO(andre: 2019-05-20): Testar se esse código ainda está funcionando
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

    num_repetitions = 10

    results_ppa_b = run_method(prey_predator_algorithm_binary, fitness_population, instance, config_ppa_b, num_repetitions)
    results_ppa_c = run_method(prey_predator_algorithm_continuous, fitness_population, instance, config_ppa_c, num_repetitions)
    results_pso = run_method(particle_swarm_optmization, fitness, instance, config_pso, num_repetitions)
    results_ga = run_method(genetic_algorithm, fitness, instance, config_ga, num_repetitions)
    results_de_random = run_method(differential_evolution, fitness_population, instance, config_de, num_repetitions, evaluate_function=evaluate_population_random)
    results_de_fixed = run_method(differential_evolution, fitness_population, instance, config_de, num_repetitions, evaluate_function=evaluate_population_fixed)

    fig = plt.figure()
    fig.suptitle('PPAC: best fitness')
    plt.plot(results_ppa_b[0], results_ppa_b[1], label="PPAB")
    plt.plot(results_ppa_c[0], results_ppa_c[1], label="PPAC")
    plt.plot(results_pso[0], results_pso[1], label="PSO")
    plt.plot(results_ga[0], results_ga[1], label="GA")
    plt.plot(results_de_random[0], results_de_random[1], label="DE Random")
    plt.plot(results_de_fixed[0], results_de_fixed[1], label="DE Fixed")
    plt.legend(loc=1)
    plt.show()
