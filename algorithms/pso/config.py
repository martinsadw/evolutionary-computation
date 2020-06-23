from enum import Enum
import configparser

from utils.misc import set_default


class Evaluator(Enum):
    RANDOM_EVALUATOR = 1
    FIXED_EVALUATOR = 2


class Config:
    def __init__(self):
        self.max_velocity = 6

        self.cost_budget = None
        self.num_iterations = None
        self.max_stagnation = None

        self.num_particles = 20

        self.inertia_parameter = 1.3
        self.local_influence_parameter = 4.1
        self.global_influence_parameter = 2.5

        self.evaluator = Evaluator.RANDOM_EVALUATOR

    @classmethod
    def load_from_file(cls, config_filename):
        config = cls()

        with open(config_filename, 'r') as config_file:
            config_string = config_file.read()
        config_values = configparser.ConfigParser(inline_comment_prefixes=(";",))
        config_values.read_string(config_string)

        config.max_velocity = float(config_values['section']['acs.pso.maxVelocity'])

        if config_values.has_option('section', 'acs.pso.costBudget'):
            config.cost_budget = int(config_values['section']['acs.pso.costBudget'])

        if config_values.has_option('section', 'acs.pso.numIterations'):
            config.num_iterations = int(config_values['section']['acs.pso.numIterations'])

        if config_values.has_option('section', 'acs.pso.maxStagnation'):
            config.max_stagnation = int(config_values['section']['acs.pso.maxStagnation'])

        config.num_particles = int(config_values['section']['acs.pso.numParticles'])

        config.inertia_parameter = float(config_values['section']['acs.pso.inertiaParameter'])
        config.local_influence_parameter = float(config_values['section']['acs.pso.localInfluenceParameter'])
        config.global_influence_parameter = float(config_values['section']['acs.pso.globalInfluenceParameter'])

        config.evaluator = Evaluator[config_values['section']['acs.pso.evaluator']]

        return config

    @classmethod
    def load_test(cls):
        config = cls()

        config.max_velocity = 2

        config.max_stagnation = 500
        config.num_particles = 30

        config.inertia_parameter = 1.0
        config.local_influence_parameter = 0.3
        config.global_influence_parameter = 0.2

        config.evaluator = Evaluator.RANDOM_EVALUATOR

        return config

    def update_from_args(self, args):
        self.max_velocity = set_default(args.max_velocity, self.max_velocity)

        self.cost_budget = set_default(args.cost_budget, self.cost_budget)
        self.num_iterations = set_default(args.num_iterations, self.num_iterations)
        self.max_stagnation = set_default(args.max_stagnation, self.max_stagnation)
        self.num_particles = set_default(args.population, self.num_particles)

        self.inertia_parameter = set_default(args.inertia, self.inertia_parameter)
        self.local_influence_parameter = set_default(args.local_influence, self.local_influence_parameter)
        self.global_influence_parameter = set_default(args.global_influence, self.global_influence_parameter)

        if args.evaluator is not None:
            self.evaluator = Evaluator[args.evaluator + '_EVALUATOR']
