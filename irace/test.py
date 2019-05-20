import argparse
import random

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
    subparsers = parser.add_subparsers(title='algorithm', dest='algorithm')
    subparsers.required = True

    parser_ga = subparsers.add_parser('ga')
    parser_ga.add_argument('config_id')
    parser_ga.add_argument('instance_id')
    parser_ga.add_argument('seed', type=int)
    parser_ga.add_argument('instance_file')
    parser_ga.add_argument('--config')
    parser_ga.add_argument('-p', '--population', type=int, default=10)
    parser_ga.add_argument('--mutation-chance', type=float, default=0.01)
    parser_ga.add_argument('--top', type=float, default=0.2)
    parser_ga.add_argument('--bottom', type=float, default=0.1)
    parser_ga.add_argument('-d', '--copying', choices=['ELITISM', 'PERMISSIVE', 'NO'], default='ELITISM')
    parser_ga.add_argument('-f', '--selection', choices=['RANDOM', 'ROULETTE'], default='ROULETTE')
    parser_ga.add_argument('-c', '--crossover', choices=['SINGLE_POINT', 'TWO_POINT', 'THREE_PARENT', 'UNIFORM'], default='TWO_POINT')
    parser_ga.add_argument('-m', '--mutation', choices=['SINGLE_BIT_INVERSION', 'MULTI_BIT_INVERSION'], default='SINGLE_BIT_INVERSION')
    parser_ga.add_argument('-r', '--repetitions', type=int, default=1)
    parser_ga.add_argument('-b', '--cost-budget', type=int)
    parser_ga.add_argument('-s', '--max-stagnation', type=int)
    parser_ga.add_argument('-i', '--num-iterations', type=int)

    args = parser.parse_args()

    instance = Instance.load_from_file(args.instance_file)
    if args.config:
        config = ga.config.Config.load_from_file(args.config)
    else:
        config = ga.config.Config().load_args(args)

    if not args.cost_budget and not args.max_stagnation and not args.num_iterations:
        raise Exception("No end conditions")

    results = np.empty((args.repetitions,))
    for i in range(args.repetitions):
        np.random.seed(args.seed + i)
        random.seed(args.seed + i)
        (population, survival_values) = genetic_algorithm(instance, config, fitness)

        results[i] = survival_values[0]

    print(results.mean())
