import configparser
from enum import Enum

from utils.misc import set_default


class Evaluator(Enum):
    RANDOM_EVALUATOR = 1
    FIXED_EVALUATOR = 2


class Config:
    def __init__(self):
        self.max_velocity = 1

        self.cost_budget = None
        self.num_iterations = None
        self.max_stagnation = None

        self.population_size = 20
        self.mutation_chance = 0.2
        self.crossover_rate = 0.05

        self.evaluator = Evaluator.FIXED_EVALUATOR

    @classmethod
    def load_from_file(cls, config_filename):
        config = cls()

        with open(config_filename, 'r') as config_file:
            config_string = config_file.read()
        config_values = configparser.ConfigParser(inline_comment_prefixes=(";",))
        config_values.read_string(config_string)

        config.max_velocity = float(config_values['section']['acs.de.maxVelocity'])

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

        config.max_velocity = 2

        config.cost_budget = 12000
        config.num_iterations = 600
        config.max_stagnation = 100

        config.population_size = 20
        config.mutation_chance = 0.8
        config.crossover_rate = 0.9

        config.evaluator = Evaluator.RANDOM_EVALUATOR

        return config

    def update_from_args(self, args):
        self.max_velocity = set_default(args.max_velocity, self.max_velocity)

        self.cost_budget = set_default(args.cost_budget, self.cost_budget)
        self.num_iterations = set_default(args.num_iterations, self.num_iterations)
        self.max_stagnation = set_default(args.max_stagnation, self.max_stagnation)

        self.population_size = set_default(args.population, self.population_size)
        self.mutation_chance = set_default(args.mutation_chance, self.mutation_chance)
        self.crossover_rate = set_default(args.crossover_rate, self.crossover_rate)

        if args.evaluator is not None:
            self.evaluator = Evaluator[args.evaluator + '_EVALUATOR']
