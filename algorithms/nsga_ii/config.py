import configparser
from enum import Enum

from utils.misc import set_default

from algorithms.ga.crossover import Crossover
from algorithms.ga.mutation import Mutation


class Config:
    def __init__(self):
        self.crossover_method = Crossover.UNIFORM_CROSSOVER
        self.mutation_method = Mutation.SINGLE_BIT_INVERSION_MUTATION

        self.cost_budget = None
        self.num_iterations = None
        self.max_stagnation = None
        self.population_size = 50

        self.mutation_chance = 0.01

    @classmethod
    def load_from_file(cls, config_filename):
        config = cls()

        with open(config_filename, 'r') as config_file:
            config_string = config_file.read()
        config_values = configparser.ConfigParser(
            inline_comment_prefixes=(";",))
        config_values.read_string(config_string)

        config.crossover_method = Crossover[config_values['section']['acs.nsgaii.crossoverMethod']]
        config.mutation_method = Mutation[config_values['section']['acs.nsgaii.mutationMethod']]

        if config_values.has_option('section', 'acs.nsgaii.costBudget'):
            config.cost_budget = int(config_values['section']['acs.nsgaii.costBudget'])

        if config_values.has_option('section', 'acs.nsgaii.numIterations'):
            config.num_iterations = int(config_values['section']['acs.nsgaii.numIterations'])

        if config_values.has_option('section', 'acs.nsgaii.maxStagnation'):
            config.max_stagnation = int(config_values['section']['acs.nsgaii.maxStagnation'])

        config.population_size = int(config_values['section']['acs.nsgaii.populationSize'])

        config.mutation_chance = float(config_values['section']['acs.nsgaii.mutationChance'])

        return config

    @classmethod
    def load_test(cls):
        config = cls()

        config.crossover_method = Crossover.TWO_POINT_CROSSOVER
        config.mutation_method = Mutation.MULTI_BIT_INVERSION_MUTATION

        config.max_stagnation = 100
        config.population_size = 20

        config.mutation_chance = 0.01

        return config

    def update_from_args(self, args):
        if args.crossover is not None:
            self.crossover_method = Crossover[args.crossover + '_CROSSOVER']
        if args.mutation is not None:
            self.mutation_method = Mutation[args.mutation + '_MUTATION']

        self.cost_budget = set_default(args.cost_budget, self.cost_budget)
        self.num_iterations = set_default(args.num_iterations, self.num_iterations)
        self.max_stagnation = set_default(args.max_stagnation, self.max_stagnation)
        self.population_size = set_default(args.population, self.population_size)

        self.mutation_chance = set_default(args.mutation_chance, self.mutation_chance)
