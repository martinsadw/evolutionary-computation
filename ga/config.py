import configparser
from enum import Enum

from ga.copying import Copying
from ga.local_search import LocalSearch
from ga.selection import Selection
from ga.crossover import Crossover
from ga.mutation import Mutation


class Config:
    def __init__(self):
        self.copying_method = Copying.ELITISM_COPYING
        self.local_search_method = LocalSearch.PER_VARIABLE_LOCAL_SEARCH

        self.selection_method = Selection.ROULETTE_SELECTION
        self.crossover_method = Crossover.TWO_POINT_CROSSOVER
        self.mutation_method = Mutation.MULTI_BIT_INVERSION_MUTATION

        self.num_iterations = 1
        self.population_size = 1

        self.top_selection_ratio = 0.1
        self.bottom_selection_ratio = 0.1
        self.mutation_chance = 0.01

        self.use_local_search = True
        self.local_search_step = 0.5
        self.local_search_quant = 1

    @classmethod
    def load_from_file(cls, config_filename):
        config = cls()

        with open(config_filename, 'r') as config_file:
            config_string = config_file.read()
        config_values = configparser.ConfigParser(
            inline_comment_prefixes=(";",))
        config_values.read_string(config_string)

        config.copying_method = Copying[config_values['section']
                                        ['acs.ga.copyingMethod']]
        config.local_search_method = LocalSearch[config_values['section']
                                                 ['acs.ga.localSearchMethod']]

        config.selection_method = Selection[config_values['section']
                                            ['acs.ga.selectionMethod']]
        config.crossover_method = Crossover[config_values['section']
                                            ['acs.ga.crossoverMethod']]
        config.mutation_method = Mutation[config_values['section']
                                          ['acs.ga.mutationMethod']]

        config.population_size = int(
            config_values['section']['acs.ga.populationSize'])
        config.num_iterations = int(
            config_values['section']['acs.ga.numIterations'])

        config.top_selection_ratio = float(
            config_values['section']['acs.ga.topSelectionRatio'])
        config.bottom_selection_ratio = float(
            config_values['section']['acs.ga.bottomSelectionRatio'])
        config.mutation_chance = float(
            config_values['section']['acs.ga.mutationChance'])

        config.use_local_search = config_values['section']['acs.ga.useLocalSearch'] == "True"
        config.local_search_step = float(
            config_values['section']['acs.ga.localSearchStep'])
        config.local_search_quant = int(
            config_values['section']['acs.ga.localSearchQuant'])

        return config

    @classmethod
    def load_test(cls):
        config = cls()

        config.copying_method = Copying.ELITISM_COPYING
        config.local_search_method = LocalSearch.PER_VARIABLE_LOCAL_SEARCH

        config.selection_method = Selection.ROULETTE_SELECTION
        config.crossover_method = Crossover.TWO_POINT_CROSSOVER
        config.mutation_method = Mutation.MULTI_BIT_INVERSION_MUTATION

        config.num_iterations = 100
        config.population_size = 20

        config.top_selection_ratio = 0.2
        config.bottom_selection_ratio = 0.1
        config.mutation_chance = 0.01

        config.use_local_search = True
        config.local_search_step = 0.5
        config.local_search_quant = 10

        return config
