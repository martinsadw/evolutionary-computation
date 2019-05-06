import argparse

import numpy as np

from acs.objective import fitness, fitness_population
from acs.instance import Instance

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_ga = subparsers.add_parser('ga')
    parser_ga.add_argument('instance_file')
    parser_ga.add_argument('config_file')
    parser_ga.add_argument('-p', '--population', type=int, default=10)
    parser_ga.add_argument('--mutation-chance', type=float, default=0.01)
    parser_ga.add_argument('--top', type=float, default=0.2)
    parser_ga.add_argument('--bottom', type=float, default=0.1)
    parser_ga.add_argument('-d', '--copying', choices=['elitism', 'permissive', 'none'], default='elitism')
    parser_ga.add_argument('-s', '--selection', choices=['random', 'roulette'], default='roulette')
    parser_ga.add_argument('-c', '--crossover', choices=['single-point', 'two-point', 'three-parent', 'uniform'], default='two-point')
    parser_ga.add_argument('-m', '--mutation', choices=['single-bit', 'multi-bit', 'three-parent', 'uniform'], default='two-point')
    parser_ga.add_argument('-r', '--repetitions', type=int, default=1)

    args = parser.parse_args()

    print('instance_file: ' + str(args.instance_file))
    print('config_file: ' + str(args.config_file))

    instance = Instance.load_from_file(args.instance_file)
    # config = ga.config.Config.load_from_file(args.config_file)
    config = ga.config.Config().load_args(args)

    results = np.empty((args.repetitions,))
    for i in range(args.repetitions):
        np.random.seed(i)
        (population, survival_values) = genetic_algorithm(instance, config, fitness)

        results[i] = survival_values[0]

    print(results.mean())
