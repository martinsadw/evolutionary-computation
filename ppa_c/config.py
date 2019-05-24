from enum import Enum
import configparser


class Evaluator(Enum):
    RANDOM_EVALUATOR = 1
    FIXED_EVALUATOR = 2


class Config:
    def __init__(self):
        self.cost_budget = None
        self.num_iterations = None
        self.max_stagnation = None

        self.population_size = 1
        self.max_position = 1

        self.follow_distance_parameter = 1
        self.follow_survival_parameter = 1

        self.min_steps = 1
        self.max_steps = 1
        self.steps_distance_parameter = 1

        self.local_search_tries = 1

        self.follow_chance = 0.5

        self.evaluator = Evaluator.RANDOM_EVALUATOR

    @classmethod
    def load_from_file(cls, config_filename):
        config = cls()

        with open(config_filename, 'r') as config_file:
            config_string = config_file.read()
        config_values = configparser.ConfigParser(inline_comment_prefixes=(";",))
        config_values.read_string(config_string)

        if config_values.has_option('section', 'acs.ppac.costBudget'):
            config.cost_budget = int(config_values['section']['acs.ppac.costBudget'])

        if config_values.has_option('section', 'acs.ppac.numIterations'):
            config.num_iterations = int(config_values['section']['acs.ppac.numIterations'])

        if config_values.has_option('section', 'acs.ppac.maxStagnation'):
            config.max_stagnation = int(config_values['section']['acs.ppac.maxStagnation'])

        config.population_size = int(config_values['section']['acs.ppac.populationSize'])
        config.max_position = int(config_values['section']['acs.ppac.maxPosition'])

        config.follow_distance_parameter = float(config_values['section']['acs.ppac.followDistanceParameter'])
        config.follow_survival_parameter = float(config_values['section']['acs.ppac.followSurvivalParameter'])

        config.min_steps = int(config_values['section']['acs.ppac.minSteps'])
        config.max_steps = int(config_values['section']['acs.ppac.maxSteps'])
        config.steps_distance_parameter = float(config_values['section']['acs.ppac.stepsDistanceParameter'])

        config.local_search_tries = int(config_values['section']['acs.ppac.localSearchTries'])

        config.follow_chance = float(config_values['section']['acs.ppac.followChance'])

        config.evaluator = Evaluator[config_values['section']['acs.ppac.evaluator']]

        return config

    @classmethod
    def load_test(cls):
        config = cls()

        config.max_stagnation = 500
        config.population_size = 5

        config.follow_distance_parameter = 1
        config.follow_survival_parameter = 1

        config.min_steps = 3
        config.max_steps = 3
        config.steps_distance_parameter = 1

        config.local_search_tries = 5

        config.follow_chance = 0.8

        return config

    @classmethod
    def load_args(cls, args):
        config = cls()

        config.max_position = args.max_velocity

        config.cost_budget = args.cost_budget
        config.num_iterations = args.num_iterations
        config.max_stagnation = args.max_stagnation
        config.population_size = args.population

        config.follow_distance_parameter = args.distance_influence
        config.follow_survival_parameter = args.survival_influence

        config.min_steps = args.min_steps
        config.max_steps = args.max_steps
        config.steps_distance_parameter = args.steps_distance

        config.local_search_tries = args.local_search

        config.follow_chance = args.follow_chance

        config.evaluator = Evaluator[args.evaluator + '_EVALUATOR']

        return config
