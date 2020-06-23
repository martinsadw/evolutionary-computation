import configparser

from utils.misc import set_default


class Config:
    def __init__(self):
        self.cost_budget = None
        self.num_iterations = None
        self.max_stagnation = None

        self.population_size = 10

        self.follow_distance_parameter = 0.6
        self.follow_survival_parameter = 0.9

        self.min_steps = 10
        self.max_steps = 15
        self.steps_distance_parameter = 0.5

        self.local_search_tries = 10

        self.follow_chance = 0.6

    @classmethod
    def load_from_file(cls, config_filename):
        config = cls()

        with open(config_filename, 'r') as config_file:
            config_string = config_file.read()
        config_values = configparser.ConfigParser(inline_comment_prefixes=(";",))
        config_values.read_string(config_string)

        if config_values.has_option('section', 'acs.ppab.costBudget'):
            config.cost_budget = int(config_values['section']['acs.ppab.costBudget'])

        if config_values.has_option('section', 'acs.ppab.numIterations'):
            config.num_iterations = int(config_values['section']['acs.ppab.numIterations'])

        if config_values.has_option('section', 'acs.ppab.maxStagnation'):
            config.max_stagnation = int(config_values['section']['acs.ppab.maxStagnation'])

        config.population_size = int(config_values['section']['acs.ppab.populationSize'])

        config.follow_distance_parameter = float(config_values['section']['acs.ppab.followDistanceParameter'])
        config.follow_survival_parameter = float(config_values['section']['acs.ppab.followSurvivalParameter'])

        config.min_steps = int(config_values['section']['acs.ppab.minSteps'])
        config.max_steps = int(config_values['section']['acs.ppab.maxSteps'])
        config.steps_distance_parameter = float(config_values['section']['acs.ppab.stepsDistanceParameter'])

        config.local_search_tries = int(config_values['section']['acs.ppab.localSearchTries'])

        config.follow_chance = float(config_values['section']['acs.ppab.followChance'])

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

    def update_from_args(self, args):
        self.cost_budget = set_default(args.cost_budget, self.cost_budget)
        self.num_iterations = set_default(args.num_iterations, self.num_iterations)
        self.max_stagnation = set_default(args.max_stagnation, self.max_stagnation)
        self.population_size = set_default(args.population, self.population_size)

        self.follow_distance_parameter = set_default(args.distance_influence, self.follow_distance_parameter)
        self.follow_survival_parameter = set_default(args.survival_influence, self.follow_survival_parameter)

        self.min_steps = set_default(args.min_steps, self.min_steps)
        self.max_steps = set_default(args.max_steps, self.max_steps)
        self.steps_distance_parameter = set_default(args.steps_distance, self.steps_distance_parameter)

        self.local_search_tries = set_default(args.local_search, self.local_search_tries)

        self.follow_chance = set_default(args.follow_chance, self.follow_chance)
