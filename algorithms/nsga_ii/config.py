import configparser
from enum import Enum

from algorithms.ga.crossover import Crossover
from algorithms.ga.mutation import Mutation


class Config:
    def __init__(self):
        self.crossover_method = Crossover.TWO_POINT_CROSSOVER
        self.mutation_method = Mutation.MULTI_BIT_INVERSION_MUTATION

        self.cost_budget = None
        self.num_iterations = None
        self.max_stagnation = None
        self.population_size = 1

        self.mutation_chance = 0.01

    @classmethod
    def load_from_file(cls, config_filename):
        config = cls()

        with open(config_filename, 'r') as config_file:
            config_string = config_file.read()
        config_values = configparser.ConfigParser(
            inline_comment_prefixes=(";",))
        config_values.read_string(config_string)

        config.crossover_method = Crossover[config_values['section']['acs.ga.crossoverMethod']]
        config.mutation_method = Mutation[config_values['section']['acs.ga.mutationMethod']]

        if config_values.has_option('section', 'acs.ga.costBudget'):
            config.cost_budget = int(config_values['section']['acs.ga.costBudget'])

        if config_values.has_option('section', 'acs.ga.numIterations'):
            config.num_iterations = int(config_values['section']['acs.ga.numIterations'])

        if config_values.has_option('section', 'acs.ga.maxStagnation'):
            config.max_stagnation = int(config_values['section']['acs.ga.maxStagnation'])

        config.population_size = int(config_values['section']['acs.ga.populationSize'])

        config.mutation_chance = float(config_values['section']['acs.ga.mutationChance'])

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

    @classmethod
    def load_args(cls, args):
        config = cls()

        config.crossover_method = Crossover[args.crossover + '_CROSSOVER']
        config.mutation_method = Mutation[args.mutation + '_MUTATION']

        config.cost_budget = args.cost_budget
        config.num_iterations = args.num_iterations
        config.max_stagnation = args.max_stagnation
        config.population_size = args.population

        config.mutation_chance = args.mutation_chance

        return config
