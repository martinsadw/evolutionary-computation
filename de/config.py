import configparser

class Config:
    def __init__(self):
        self.max_stagnation = 1
        self.population_size = 1
        self.mutation_chance=0.8
        self.crossover_rate=0.9
    
    @classmethod
    def load_from_file(cls, config_filename):
        config = cls()

        with open(config_filename, 'r') as config_file:
            config_string = config_file.read()
        config_values = configparser.ConfigParser(inline_comment_prefixes=(";",))
        config_values.read_string(config_string)

        config.max_stagnation = int(config_values['section']['acs.de.maxStagnation'])
        config.population_size = int(config_values['section']['acs.de.populationSize'])
        config.mutation_chance = float(config_values['section']['acs.de.mutationChance'])
        config.crossover_rate = float(config_values['section']['acs.de.crossoverRate'])


        return config

    @classmethod
    def load_test(cls):
        config = cls()

        config.max_stagnation = 100
        config.population_size = 20
        config.mutation_chance = 0.8
        config.crossover_rate=0.9

        return config
