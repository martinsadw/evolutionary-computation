import sys
import pickle

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness
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

    config_ppa_b.cost_budget = 100000
    config_ppa_c.cost_budget = 100000
    config_pso.cost_budget = 100000
    config_ga.cost_budget = 100000
    config_de.cost_budget = 100000

    num_repetitions = 10

    use_cache = False
    filename = 'results/real_test_10_10000.pickle'

    if not use_cache:
        results_ppa_b = run_method(prey_predator_algorithm_binary, fitness, instance, config_ppa_b, num_repetitions)
        results_ppa_c = run_method(prey_predator_algorithm_continuous, fitness, instance, config_ppa_c, num_repetitions)
        results_pso = run_method(particle_swarm_optmization, fitness, instance, config_pso, num_repetitions)
        results_ga = run_method(genetic_algorithm, fitness, instance, config_ga, num_repetitions)
        results_de = run_method(differential_evolution, fitness, instance, config_de, num_repetitions)

        results = {
            'ppa_b': results_ppa_b,
            'ppa_c': results_ppa_c,
            'pso': results_pso,
            'ga': results_ga,
            'de': results_de,
        }
        with open(filename, 'wb') as file:
            pickle.dump(results, file)
    else:
        with open(filename, 'rb') as file:
            results = pickle.load(file)

        results_ppa_b = results['ppa_b']
        results_ppa_c = results['ppa_c']
        results_pso = results['pso']
        results_ga = results['ga']
        results_de = results['de']


    mean_ppa_b = np.mean(results_ppa_b[1], axis=(0, 1))
    mean_ppa_c = np.mean(results_ppa_c[1], axis=(0, 1))
    mean_pso = np.mean(results_pso[1], axis=(0, 1))
    mean_ga = np.mean(results_ga[1], axis=(0, 1))
    mean_de = np.mean(results_de[1], axis=(0, 1))

    deviation_ppa_b = np.std(results_ppa_b[1], axis=(0, 1))
    deviation_ppa_c = np.std(results_ppa_c[1], axis=(0, 1))
    deviation_pso = np.std(results_pso[1], axis=(0, 1))
    deviation_ga = np.std(results_ga[1], axis=(0, 1))
    deviation_de = np.std(results_de[1], axis=(0, 1))

    mean_partial_ppa_b = np.mean(results_ppa_b[2], axis=(0, 1))
    mean_partial_ppa_c = np.mean(results_ppa_c[2], axis=(0, 1))
    mean_partial_pso = np.mean(results_pso[2], axis=(0, 1))
    mean_partial_ga = np.mean(results_ga[2], axis=(0, 1))
    mean_partial_de = np.mean(results_de[2], axis=(0, 1))

    # Colorblind colors: https://gist.github.com/thriveth/8560036
    # fig.suptitle('PPAC: best fitness')
    plt.xlabel('# execuções da função de avaliação')
    plt.ylabel('valor da avaliação')
    plt.plot(results_ppa_b[0], mean_ppa_b, color='#4daf4a', label="APPD")
    plt.plot(results_ppa_c[0], mean_ppa_c, color='#f781bf', label="APPC")
    plt.plot(results_pso[0], mean_pso, color='#a65628', label="OEP")
    plt.plot(results_ga[0], mean_ga, color='#377eb8', label="AG")
    plt.plot(results_de[0], mean_de, color='#ff7f00', label="ED")
    plt.legend(loc=1)
    plt.show()

    print(mean_partial_ga[0, 0])
    print(mean_partial_ga[0, 1])
    print(mean_partial_ga[0, 2])
    print(mean_partial_ga[0, 3])
    print(mean_partial_ga[0, 4])

    plt.xlabel('# execuções da função de avaliação')
    plt.ylabel('valor da avaliação')
    plt.plot(results_ga[0], mean_ga, color='#377eb8', label="AG")
    plt.plot(results_ga[0], mean_ga + deviation_ga, linestyle='--', color='#377eb8', linewidth=0.5)
    plt.plot(results_ga[0], mean_ga - deviation_ga, linestyle='--', color='#377eb8', linewidth=0.5)
    plt.fill_between(results_ga[0], mean_ga + deviation_ga, mean_ga - deviation_ga, facecolor='#377eb8', alpha=0.2)
    plt.plot(results_de[0], mean_de, color='#ff7f00', label="ED")
    plt.plot(results_de[0], mean_de - deviation_de, linestyle='--', color='#ff7f00', linewidth=0.5)
    plt.plot(results_de[0], mean_de + deviation_de, linestyle='--', color='#ff7f00', linewidth=0.5)
    plt.fill_between(results_de[0], mean_de + deviation_de, mean_de - deviation_de, facecolor='#ff7f00', alpha=0.2)
    plt.legend(loc=1)
    plt.show()

    plt.xlabel('# execuções da função de avaliação')
    plt.ylabel('valor da avaliação')
    plt.plot(results_de[0], mean_partial_de[:, 0], color='#377eb8', label="Cobertura")
    plt.plot(results_de[0], mean_partial_de[:, 1], color='#ff7f00', label="Dificuldade")
    plt.plot(results_de[0], mean_partial_de[:, 2], color='#4daf4a', label="Tempo")
    plt.plot(results_de[0], mean_partial_de[:, 3], color='#f781bf', label="Balanceamento")
    plt.plot(results_de[0], mean_partial_de[:, 4], color='#a65628', label="Estilo")
    plt.legend(loc=1)
    plt.show()
