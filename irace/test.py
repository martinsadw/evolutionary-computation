import argparse
import random

import numpy as np

from acs.objective import fitness, fitness_population
from acs.instance import Instance

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


def create_base_parser(parser):
    parser.add_argument('config_id')
    parser.add_argument('instance_id')
    parser.add_argument('seed', type=int)
    parser.add_argument('instance_file')
    parser.add_argument('--config')
    parser.add_argument('-p', '--population', type=int, default=10)
    parser.add_argument('-r', '--repetitions', type=int, default=1)
    parser.add_argument('-b', '--cost-budget', type=int)
    parser.add_argument('-s', '--max-stagnation', type=int)
    parser.add_argument('-i', '--num-iterations', type=int)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='algorithm', dest='algorithm')
    subparsers.required = True

    config_class_dict = {
        'ga': ga.config.Config,
        'pso': pso.config.Config,
    }

    parser_ga = subparsers.add_parser('ga')
    create_base_parser(parser_ga)
    parser_ga.add_argument('--mutation-chance', type=float, default=0.01)
    parser_ga.add_argument('--top', type=float, default=0.2)
    parser_ga.add_argument('--bottom', type=float, default=0.1)
    parser_ga.add_argument('-d', '--copying', choices=['ELITISM', 'PERMISSIVE', 'NO'], default='ELITISM')
    parser_ga.add_argument('-f', '--selection', choices=['RANDOM', 'ROULETTE'], default='ROULETTE')
    parser_ga.add_argument('-c', '--crossover', choices=['SINGLE_POINT', 'TWO_POINT', 'THREE_PARENT', 'UNIFORM'], default='TWO_POINT')
    parser_ga.add_argument('-m', '--mutation', choices=['SINGLE_BIT_INVERSION', 'MULTI_BIT_INVERSION'], default='SINGLE_BIT_INVERSION')

    parser_pso = subparsers.add_parser('pso')
    create_base_parser(parser_pso)
    parser_pso.add_argument('-v', '--max-velocity', type=float, default=6)
    parser_pso.add_argument('-n', '--inertia', type=float, default=1)
    parser_pso.add_argument('-l', '--local-influence', type=float, default=1)
    parser_pso.add_argument('-g', '--global-influence', type=float, default=1)
    parser_pso.add_argument('-e', '--evaluator', choices=['RANDOM', 'FIXED'], default='RANDOM')

    args = parser.parse_args()

    if not args.cost_budget and not args.max_stagnation and not args.num_iterations:
        raise Exception("No end conditions")

    instance = Instance.load_from_file(args.instance_file)

    config_class = config_class_dict[args.algorithm]
    if args.config:
        config = config_class.load_from_file(args.config)
    else:
        config = config_class.load_args(args)

    if args.algorithm == 'ppa_b':
        results = run_method(prey_predator_algorithm_binary, fitness_population, instance, config, args.repetitions, seed=args.seed)
    elif args.algorithm == 'ppa_c_random':
        results = run_method(prey_predator_algorithm_continuous, fitness_population, instance, config, args.repetitions, seed=args.seed, evaluate_function=evaluate_population_random)
    elif args.algorithm == 'ppa_c_fixed':
        results = run_method(prey_predator_algorithm_continuous, fitness_population, instance, config, args.repetitions, seed=args.seed, evaluate_function=evaluate_population_fixed)
    elif args.algorithm == 'pso':
        results = run_method(particle_swarm_optmization, fitness, instance, config, args.repetitions, seed=args.seed)
    elif args.algorithm == 'ga':
        results = run_method(genetic_algorithm, fitness, instance, config, args.repetitions, seed=args.seed)
    elif args.algorithm == 'de_random':
        results = run_method(differential_evolution, fitness_population, instance, config, args.repetitions, seed=args.seed, evaluate_function=evaluate_population_random)
    elif args.algorithm == 'de_fixed':
        results = run_method(differential_evolution, fitness_population, instance, config, args.repetitions, seed=args.seed, evaluate_function=evaluate_population_fixed)

    print(results[1][-1])
