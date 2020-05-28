import argparse
import random

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness, multi_fitness
from acs.instance import Instance

from utils.misc import evaluate_population_fixed, evaluate_population_random
from utils.runner import run_method

from algorithms.ppa_d.main import prey_predator_algorithm_discrete
from algorithms.ppa_c.main import prey_predator_algorithm_continuous
from algorithms.pso.main import particle_swarm_optmization
from algorithms.ga.main import genetic_algorithm
from algorithms.de.main import differential_evolution

import algorithms.ppa_d.config as ppa_d_config
import algorithms.ppa_c.config as ppa_c_config
import algorithms.pso.config as pso_config
import algorithms.ga.config as ga_config
import algorithms.de.config as de_config


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
    parser.add_argument('--show', action='store_true')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='algorithm', dest='algorithm')
    subparsers.required = True

    config_class_dict = {
        'ga': ga_config.Config,
        'pso': pso_config.Config,
        'ppa_d': ppa_d_config.Config,
        'ppa_c': ppa_c_config.Config,
        'de': de_config.Config,
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

    parser_ppa_d = subparsers.add_parser('ppa_d')
    create_base_parser(parser_ppa_d)
    parser_ppa_d.add_argument('-d', '--distance-influence', type=float, default=1)
    parser_ppa_d.add_argument('-f', '--survival-influence', type=float, default=1)
    parser_ppa_d.add_argument('-n', '--min-steps', type=int, default=4)
    parser_ppa_d.add_argument('-x', '--max-steps', type=int, default=25)
    parser_ppa_d.add_argument('-t', '--steps-distance', type=float, default=0.1)
    parser_ppa_d.add_argument('-l', '--local-search', type=int, default=5)
    parser_ppa_d.add_argument('-c', '--follow-chance', type=float, default=0.8)

    parser_ppa_c = subparsers.add_parser('ppa_c')
    create_base_parser(parser_ppa_c)
    parser_ppa_c.add_argument('-v', '--max-velocity', type=float, default=6)
    parser_ppa_c.add_argument('-d', '--distance-influence', type=float, default=1)
    parser_ppa_c.add_argument('-f', '--survival-influence', type=float, default=1)
    parser_ppa_c.add_argument('-n', '--min-steps', type=int, default=4)
    parser_ppa_c.add_argument('-x', '--max-steps', type=int, default=25)
    parser_ppa_c.add_argument('-t', '--steps-distance', type=float, default=0.1)
    parser_ppa_c.add_argument('-l', '--local-search', type=int, default=5)
    parser_ppa_c.add_argument('-c', '--follow-chance', type=float, default=0.8)
    parser_ppa_c.add_argument('-e', '--evaluator', choices=['RANDOM', 'FIXED'], default='RANDOM')

    parser_de = subparsers.add_parser('de')
    create_base_parser(parser_de)
    parser_de.add_argument('-v', '--max-velocity', type=float, default=6)
    parser_de.add_argument('-m', '--mutation-chance', type=float, default=0.1)
    parser_de.add_argument('-c', '--crossover-rate', type=float, default=0.5)
    parser_de.add_argument('-e', '--evaluator', choices=['RANDOM', 'FIXED'], default='RANDOM')

    args = parser.parse_args()

    if not args.config and not args.cost_budget and not args.max_stagnation and not args.num_iterations:
        raise Exception("No end condition specified. Use '-b', '-s' or '-i'.")

    instance = Instance.load_from_file(args.instance_file)

    # TODO(andre:2019-10-29): Fazer com que os parametros da linha de comando
    # sobrescrevam os parametros do arquivo de configuração ao invés de serem ignorados
    config_class = config_class_dict[args.algorithm]
    if args.config:
        config = config_class.load_from_file(args.config)
    else:
        config = config_class.load_args(args)

    if args.algorithm == 'ppa_d':
        label = 'PPAB'
        results = run_method(prey_predator_algorithm_discrete, fitness, instance, config, args.repetitions, seed=args.seed, result_format='full')
    elif args.algorithm == 'ppa_c':
        label = 'PPAC'
        results = run_method(prey_predator_algorithm_continuous, fitness, instance, config, args.repetitions, seed=args.seed, result_format='full')
    elif args.algorithm == 'pso':
        label = 'PSO'
        results = run_method(particle_swarm_optmization, fitness, instance, config, args.repetitions, seed=args.seed, result_format='full')
    elif args.algorithm == 'ga':
        label = 'GA'
        results = run_method(genetic_algorithm, multi_fitness, instance, config, args.repetitions, seed=args.seed, result_format='full')
    elif args.algorithm == 'de':
        label = 'DE'
        results = run_method(differential_evolution, fitness, instance, config, args.repetitions, seed=args.seed, result_format='full')

    mean_best_fitness = np.mean(results[2], axis=(0, 1))
    mean_partial_fitness = np.mean(results[3], axis=(0, 1))

    print(mean_best_fitness[-1])

    if args.show:
        fig = plt.figure()
        fig.suptitle('%s: best fitness' % label)
        plt.plot(results[1], mean_best_fitness, label=label)
        plt.legend(loc=1)
        plt.show()

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
