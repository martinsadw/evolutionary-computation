import configparser


class Config:
    def __init__(self):
        # self.num_iterations = 1
        self.max_stagnation = 1
        self.population_size = 1

        self.follow_distance_parameter = 1
        self.follow_survival_parameter = 1

        self.min_steps = 1
        self.max_steps = 1
        self.steps_distance_parameter = 1

        self.local_search_tries = 1

        self.follow_chance = 0.5

    @classmethod
    def load_from_file(cls, config_filename):
        config = cls()

        with open(config_filename, 'r') as config_file:
            config_string = config_file.read()
        config_values = configparser.ConfigParser(inline_comment_prefixes=(";",))
        config_values.read_string(config_string)

        # config.num_iterations = int(config_values['section']['ppatosca.arg.numIterations'])
        config.max_stagnation = int(config_values['section']['ppatosca.arg.maxStagnation'])
        config.population_size = int(config_values['section']['ppatosca.arg.populationSize'])

        config.follow_distance_parameter = float(config_values['section']['ppatosca.arg.followDistanceParameter'])
        config.follow_survival_parameter = float(config_values['section']['ppatosca.arg.followSurvivalParameter'])

        config.min_steps = int(config_values['section']['ppatosca.arg.minSteps'])
        config.max_steps = int(config_values['section']['ppatosca.arg.maxSteps'])
        config.steps_distance_parameter = float(config_values['section']['ppatosca.arg.stepsDistanceParameter'])

        config.local_search_tries = int(config_values['section']['ppatosca.arg.localSearchTries'])

        config.follow_chance = float(config_values['section']['ppatosca.arg.followChance'])

        return config

    @classmethod
    def load_test(cls):
        config = cls()

        # config.num_iterations = 0
        config.max_stagnation = 0
        config.population_size = 5

        config.follow_distance_parameter = 1
        config.follow_survival_parameter = 1

        config.min_steps = 3
        config.max_steps = 3
        config.steps_distance_parameter = 1

        config.local_search_tries = 5

        config.follow_chance = 0.8

        return config
