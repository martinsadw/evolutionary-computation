import configparser
from enum import Enum


class Evaluator(Enum):
    RANDOM_EVALUATOR = 1
    FIXED_EVALUATOR = 2


class Config:
    def __init__(self):
        self.cost_budget = None
        self.num_iterations = None
        self.max_stagnation = None

        self.population_size = 1
        self.mutation_chance = 0.8
        self.crossover_rate = 0.9

        self.evaluator = Evaluator.RANDOM_EVALUATOR

    @classmethod
    def load_from_file(cls, config_filename):
        config = cls()

        with open(config_filename, 'r') as config_file:
            config_string = config_file.read()
        config_values = configparser.ConfigParser(inline_comment_prefixes=(";",))
        config_values.read_string(config_string)

        if config_values.has_option('section', 'acs.de.costBudget'):
            config.cost_budget = int(config_values['section']['acs.de.costBudget'])

        if config_values.has_option('section', 'acs.de.numIterations'):
            config.num_iterations = int(config_values['section']['acs.de.numIterations'])

        if config_values.has_option('section', 'acs.de.maxStagnation'):
            config.max_stagnation = int(config_values['section']['acs.de.maxStagnation'])

        config.population_size = int(config_values['section']['acs.de.populationSize'])
        config.mutation_chance = float(config_values['section']['acs.de.mutationChance'])
        config.crossover_rate = float(config_values['section']['acs.de.crossoverRate'])

        config.evaluator = Evaluator[config_values['section']['acs.de.evaluator']]

        return config

    @classmethod
    def load_test(cls):
        config = cls()

        config.cost_budget = 12000
        config.num_iterations = 600
        config.max_stagnation = 100
        config.population_size = 20
        config.mutation_chance = 0.8
        config.crossover_rate = 0.9

        config.evaluator = Evaluator.RANDOM_EVALUATOR

        return config

    @classmethod
    def load_args(cls, args):
        config = cls()

        config.cost_budget = args.cost_budget
        config.num_iterations = args.num_iterations
        config.max_stagnation = args.max_stagnation
        config.population_size = args.population
        config.mutation_chance = args.mutation_chance
        config.crossover_rate = args.crossover_rate

        config.evaluator = Evaluator[args.evaluator + '_EVALUATOR']

        return config
