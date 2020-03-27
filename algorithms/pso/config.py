from enum import Enum
import configparser


class Evaluator(Enum):
    RANDOM_EVALUATOR = 1
    FIXED_EVALUATOR = 2


class Config:
    def __init__(self):
        self.max_velocity = 1

        self.cost_budget = None
        self.num_iterations = None
        self.max_stagnation = None

        self.num_particles = 1

        self.inertia_parameter = 1
        self.local_influence_parameter = 1
        self.global_influence_parameter = 1

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

    @classmethod
    def load_args(cls, args):
        config = cls()

        config.max_velocity = args.max_velocity

        config.cost_budget = args.cost_budget
        config.num_iterations = args.num_iterations
        config.max_stagnation = args.max_stagnation
        config.num_particles = args.population

        config.inertia_parameter = args.inertia
        config.local_influence_parameter = args.local_influence
        config.global_influence_parameter = args.global_influence

        config.evaluator = Evaluator[args.evaluator + '_EVALUATOR']

        return config
