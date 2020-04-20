import argparse
import datetime
import os
import pickle
import sys

from acs.objective import fitness
from acs.instance import Instance

from utils.runner import run_method

from algorithms.ppa_d.main import prey_predator_algorithm_discrete
from algorithms.pso.main import particle_swarm_optmization
from algorithms.ga.main import genetic_algorithm
from algorithms.de.main import differential_evolution

import algorithms.ppa_d.config as ppa_d_config
import algorithms.pso.config as pso_config
import algorithms.ga.config as ga_config
import algorithms.de.config as de_config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('instance_file')
    parser.add_argument('-r', '--repetitions', type=int, default=1)
    parser.add_argument('-b', '--cost-budget', type=int)
    parser.add_argument('-s', '--max-stagnation', type=int)
    parser.add_argument('-i', '--num-iterations', type=int)
    parser.add_argument('-f', '--results-format', choices=['simple', 'full'], default='simple')
    parser.add_argument('-n', '--results-name', default='results/comparison.pickle')
    parser.add_argument('--no-ppad', action='store_true')
    parser.add_argument('--no-pso', action='store_true')
    parser.add_argument('--no-ga', action='store_true')
    parser.add_argument('--no-de', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    if not args.cost_budget and not args.max_stagnation and not args.num_iterations:
        raise Exception('No end condition specified. Use "-b", "-s" or "-i".')

    instance = Instance.load_from_file(args.instance_file)

    configs = []
    if not args.no_ppad:
        configs.append(('ppa_d', prey_predator_algorithm_discrete, ppa_d_config.Config.load_from_file('instances/ppa_d_config.txt')))
    if not args.no_pso:
        configs.append(('pso', particle_swarm_optmization, pso_config.Config.load_from_file('instances/pso_config.txt')))
    if not args.no_ga:
        configs.append(('ga', genetic_algorithm, ga_config.Config.load_from_file('instances/ga_config.txt')))
    if not args.no_de:
        configs.append(('de', differential_evolution, de_config.Config.load_from_file('instances/de_config.txt')))

    if len(configs) <= 0:
        raise Exception('No algorithms specified. Select at least one algorithm')

    results = {
        'info': {
            'command': os.path.basename(sys.argv[0]) + " " + " ".join(sys.argv[1:]),
            'datetime': str(datetime.datetime.now()),
            'instance': instance,
            'repetitions': args.repetitions,
            'cost_budget': args.cost_budget,
            'max_stagnation': args.max_stagnation,
            'num_iterations': args.num_iterations,
            'results_format': args.results_format,
            'results_name': args.results_name,
            'algorithms': [],
        },
    }
    for (name, function, config) in configs:
        config.cost_budget = args.cost_budget
        config.max_stagnation = args.max_stagnation
        config.num_iterations = args.num_iterations

        if args.verbose:
            print('Running %s' % name)

        results[name] = run_method(function, fitness, instance, config, args.repetitions, verbose=args.verbose)
        results['info']['algorithms'].append(name)

    os.makedirs(os.path.dirname(args.results_name), exist_ok=True)
    with open(args.results_name, 'wb') as file:
        pickle.dump(results, file)
