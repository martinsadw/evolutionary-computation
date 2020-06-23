import argparse
import datetime
import os
import pickle
import random
import sys

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, multi_fitness
from acs.instance import Instance

from utils.multiobjective import fitness_sch
from utils.misc import evaluate_population_fixed, evaluate_population_random
from utils.runner import run_method, run_multiobjective_method

from algorithms.ppa_d.main import prey_predator_algorithm_discrete
from algorithms.ppa_c.main import prey_predator_algorithm_continuous
from algorithms.pso.main import particle_swarm_optmization
from algorithms.ga.main import genetic_algorithm
from algorithms.de.main import differential_evolution
from algorithms.nsga_ii.main import nsga_ii

import algorithms.ppa_d.config as ppa_d_config
import algorithms.ppa_c.config as ppa_c_config
import algorithms.pso.config as pso_config
import algorithms.ga.config as ga_config
import algorithms.de.config as de_config
import algorithms.nsga_ii.config as nsga_ii_config


def create_base_parser(parser):
    parser.add_argument('config_id')
    parser.add_argument('instance_id')
    parser.add_argument('seed', type=int)
    parser.add_argument('instance_file')
    parser.add_argument('--config')
    parser.add_argument('-p', '--population', type=int)
    parser.add_argument('-r', '--repetitions', type=int, default=1)
    parser.add_argument('-b', '--cost-budget', type=int)
    parser.add_argument('-s', '--max-stagnation', type=int)
    parser.add_argument('-i', '--num-iterations', type=int)
    parser.add_argument('--show', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-n', '--results-name', default='results/comparison.pickle')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='algorithm', dest='algorithm')
    subparsers.required = True

    config_class_dict = {
        'ga': ga_config.Config,
        'nsga_ii': nsga_ii_config.Config,
        'pso': pso_config.Config,
        'ppa_d': ppa_d_config.Config,
        'ppa_c': ppa_c_config.Config,
        'de': de_config.Config,
    }

    parser_ga = subparsers.add_parser('ga')
    create_base_parser(parser_ga)
    parser_ga.add_argument('--mutation-chance', type=float)
    parser_ga.add_argument('--top', type=float)
    parser_ga.add_argument('--bottom', type=float)
    parser_ga.add_argument('-d', '--copying', choices=['ELITISM', 'PERMISSIVE', 'NO'])
    parser_ga.add_argument('-f', '--selection', choices=['RANDOM', 'ROULETTE'])
    parser_ga.add_argument('-c', '--crossover', choices=['SINGLE_POINT', 'TWO_POINT', 'THREE_PARENT', 'UNIFORM'])
    parser_ga.add_argument('-m', '--mutation', choices=['SINGLE_BIT_INVERSION', 'MULTI_BIT_INVERSION'])

    parser_nsga_ii = subparsers.add_parser('nsga_ii')
    create_base_parser(parser_nsga_ii)
    parser_nsga_ii.add_argument('--mutation-chance', type=float)
    parser_nsga_ii.add_argument('-c', '--crossover', choices=['SINGLE_POINT', 'TWO_POINT', 'THREE_PARENT', 'UNIFORM'])
    parser_nsga_ii.add_argument('-m', '--mutation', choices=['SINGLE_BIT_INVERSION', 'MULTI_BIT_INVERSION'])
    parser_nsga_ii.add_argument('-o', '--num-objectives', type=int, default=2)

    parser_pso = subparsers.add_parser('pso')
    create_base_parser(parser_pso)
    parser_pso.add_argument('-m', '--max-velocity', type=float)
    parser_pso.add_argument('-t', '--inertia', type=float)
    parser_pso.add_argument('-l', '--local-influence', type=float)
    parser_pso.add_argument('-g', '--global-influence', type=float)
    parser_pso.add_argument('-a', '--evaluator', choices=['RANDOM', 'FIXED'])

    parser_ppa_d = subparsers.add_parser('ppa_d')
    create_base_parser(parser_ppa_d)
    parser_ppa_d.add_argument('-d', '--distance-influence', type=float)
    parser_ppa_d.add_argument('-f', '--survival-influence', type=float)
    parser_ppa_d.add_argument('-t', '--min-steps', type=int)
    parser_ppa_d.add_argument('-x', '--max-steps', type=int)
    parser_ppa_d.add_argument('-e', '--steps-distance', type=float)
    parser_ppa_d.add_argument('-l', '--local-search', type=int)
    parser_ppa_d.add_argument('-c', '--follow-chance', type=float)

    parser_ppa_c = subparsers.add_parser('ppa_c')
    create_base_parser(parser_ppa_c)
    parser_ppa_c.add_argument('-m', '--max-velocity', type=float)
    parser_ppa_c.add_argument('-d', '--distance-influence', type=float)
    parser_ppa_c.add_argument('-f', '--survival-influence', type=float)
    parser_ppa_c.add_argument('-t', '--min-steps', type=int)
    parser_ppa_c.add_argument('-x', '--max-steps', type=int)
    parser_ppa_c.add_argument('-e', '--steps-distance', type=float)
    parser_ppa_c.add_argument('-l', '--local-search', type=int)
    parser_ppa_c.add_argument('-c', '--follow-chance', type=float)
    parser_ppa_c.add_argument('-a', '--evaluator', choices=['RANDOM', 'FIXED'])

    parser_de = subparsers.add_parser('de')
    create_base_parser(parser_de)
    parser_de.add_argument('-m', '--max-velocity', type=float)
    parser_de.add_argument('--mutation-chance', type=float)
    parser_de.add_argument('-c', '--crossover-rate', type=float)
    parser_de.add_argument('-a', '--evaluator', choices=['RANDOM', 'FIXED'])

    args = parser.parse_args()

    if not args.config and not args.cost_budget and not args.max_stagnation and not args.num_iterations:
        raise Exception("No end condition specified. Use '-b', '-s' or '-i'.")

    if args.algorithm == 'nsga_ii' and args.num_objectives > 5:
        raise Exception("The problem can only have at most five objectives")

    instance = Instance.load_from_file(args.instance_file)

    config_class = config_class_dict[args.algorithm]
    if args.config:
        config = config_class.load_from_file(args.config)
    else:
        config = config_class()

    config.update_from_args(args)

    results = {
        'info': {
            'command': os.path.basename(sys.argv[0]) + " " + " ".join(sys.argv[1:]),
            'datetime': str(datetime.datetime.now()),
            'instance': instance,
            'config_id': args.config_id,
            'instance_id': args.instance_id,
            'seed': args.seed,
            'config': config,
            'results_name': args.results_name,
            'algorithm': args.algorithm,
        },
    }

    if args.algorithm == 'ppa_d':
        results['info']['multiobjective'] = False
        label = 'PPAB'
        results['data'] = run_method(prey_predator_algorithm_discrete, fitness, instance, config, args.repetitions, verbose=args.verbose, seed=args.seed, result_format='full')
    elif args.algorithm == 'ppa_c':
        results['info']['multiobjective'] = False
        label = 'PPAC'
        results['data'] = run_method(prey_predator_algorithm_continuous, fitness, instance, config, args.repetitions, verbose=args.verbose, seed=args.seed, result_format='full')
    elif args.algorithm == 'pso':
        results['info']['multiobjective'] = False
        label = 'PSO'
        results['data'] = run_method(particle_swarm_optmization, fitness, instance, config, args.repetitions, verbose=args.verbose, seed=args.seed, result_format='full')
    elif args.algorithm == 'ga':
        results['info']['multiobjective'] = False
        label = 'GA'
        results['data'] = run_method(genetic_algorithm, fitness, instance, config, args.repetitions, verbose=args.verbose, seed=args.seed, result_format='full')
    elif args.algorithm == 'de':
        results['info']['multiobjective'] = False
        label = 'DE'
        results['data'] = run_method(differential_evolution, fitness, instance, config, args.repetitions, verbose=args.verbose, seed=args.seed, result_format='full')
    elif args.algorithm == 'nsga_ii':
        results['info']['multiobjective'] = True
        results['info']['num_objectives'] = args.num_objectives
        label = 'NSGA-II'
        # instance.num_learners = 1
        results['data'] = run_multiobjective_method(nsga_ii, multi_fitness, instance, config, args.repetitions, verbose=args.verbose, num_objectives=args.num_objectives, seed=args.seed, result_format='full')
        # instance.num_materials = 20
        # results = run_multiobjective_method(nsga_ii, fitness_sch, instance, config, args.repetitions, num_objectives=args.num_objectives, seed=args.seed, result_format='full')


    os.makedirs(os.path.dirname(args.results_name), exist_ok=True)
    with open(args.results_name, 'wb') as file:
        pickle.dump(results, file)

    # mean_best_fitness = np.mean(results[2], axis=(0, 1))
    # mean_partial_fitness = np.mean(results[3], axis=(0, 1))
    #
    # print(mean_best_fitness[-1])
    #
    # if args.show:
    #     fig = plt.figure()
    #     fig.suptitle('%s: best fitness' % label)
    #     plt.plot(results[1], mean_best_fitness, label=label)
    #     plt.legend(loc=1)
    #     plt.show()

    # if args.show:
    #     fig = plt.figure()
    #     fig.suptitle('%s: best fitness' % label)
    #     plt.plot(results[0], mean_best_fitness, label="Total")
    #     plt.plot(results[0], mean_partial_fitness[:, 0], label="Coverage")
    #     plt.plot(results[0], mean_partial_fitness[:, 1], label="Difficulty")
    #     plt.plot(results[0], mean_partial_fitness[:, 2], label="Time")
    #     plt.plot(results[0], mean_partial_fitness[:, 3], label="Balance")
    #     plt.plot(results[0], mean_partial_fitness[:, 4], label="Style")
    #     plt.legend(loc=1)
    #     plt.show()

    # temp = results[3].mean(axis=0)
    # for i in range(24):
    #     plt.xlabel('# execuções da função de avaliação')
    #     plt.ylabel('valor da avaliação')
    #     plt.ylim((-1, 7))
    #     plt.plot(results[1], temp[i, :, 0], color='#377eb8', label="Cobertura")
    #     plt.plot(results[1], temp[i, :, 1], color='#ff7f00', label="Dificuldade")
    #     plt.plot(results[1], temp[i, :, 2], color='#4daf4a', label="Tempo")
    #     plt.plot(results[1], temp[i, :, 3], color='#f781bf', label="Balanceamento")
    #     plt.plot(results[1], temp[i, :, 4], color='#a65628', label="Estilo")
    #     plt.legend(loc=1)
    #     # plt.show()
    #     # plt.savefig('results/de_partial_all.png')
    #     plt.savefig('results/de_partial_%d.png' % i)
    #     plt.close()
