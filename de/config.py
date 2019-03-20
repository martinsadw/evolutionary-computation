import configparser
from enum import Enum

class Config:
    def __init__(self):
        self.max_stagnation = 1
        self.population_size = 1
    
    @classmethod
    def load_from_file(cls, config_filename):
        config = cls()

        with open(config_filename, 'r') as config_file:
            config_string = config_file.read()
        config_values = configparser.ConfigParser(
            inline_comment_prefixes=(";",))
        config_values.read_string(config_string)

        config.max_stagnation = int(config_values['section']['acs.ga.maxStagnation'])
        config.population_size = int(config_values['section']['acs.ga.populationSize'])

        return config

    @classmethod
    def load_test(cls):
        config = cls()

        config.max_stagnation = 100
        config.population_size = 20

        return config
