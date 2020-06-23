import configparser
from enum import Enum

from utils.misc import set_default

from algorithms.ga.copying import Copying
from algorithms.ga.local_search import LocalSearch
from algorithms.ga.selection import Selection
from algorithms.ga.crossover import Crossover
from algorithms.ga.mutation import Mutation


class Config:
    def __init__(self):
        self.copying_method = Copying.PERMISSIVE_COPYING
        self.local_search_method = LocalSearch.PER_VARIABLE_LOCAL_SEARCH

        self.selection_method = Selection.ROULETTE_SELECTION
        self.crossover_method = Crossover.UNIFORM_CROSSOVER
        self.mutation_method = Mutation.SINGLE_BIT_INVERSION_MUTATION

        self.cost_budget = None
        self.num_iterations = None
        self.max_stagnation = None

        self.population_size = 10
        self.top_selection_ratio = 0.15
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

        config.copying_method = Copying[config_values['section']['acs.ga.copyingMethod']]
        config.local_search_method = LocalSearch[config_values['section']['acs.ga.localSearchMethod']]

        config.selection_method = Selection[config_values['section']['acs.ga.selectionMethod']]
        config.crossover_method = Crossover[config_values['section']['acs.ga.crossoverMethod']]
        config.mutation_method = Mutation[config_values['section']['acs.ga.mutationMethod']]

        if config_values.has_option('section', 'acs.ga.costBudget'):
            config.cost_budget = int(config_values['section']['acs.ga.costBudget'])

        if config_values.has_option('section', 'acs.ga.numIterations'):
            config.num_iterations = int(config_values['section']['acs.ga.numIterations'])

        if config_values.has_option('section', 'acs.ga.maxStagnation'):
            config.max_stagnation = int(config_values['section']['acs.ga.maxStagnation'])

        config.population_size = int(config_values['section']['acs.ga.populationSize'])
        config.top_selection_ratio = float(config_values['section']['acs.ga.topSelectionRatio'])
        config.bottom_selection_ratio = float(config_values['section']['acs.ga.bottomSelectionRatio'])
        config.mutation_chance = float(config_values['section']['acs.ga.mutationChance'])

        config.use_local_search = config_values['section']['acs.ga.useLocalSearch'] == "True"
        config.local_search_step = float(config_values['section']['acs.ga.localSearchStep'])
        config.local_search_quant = int(config_values['section']['acs.ga.localSearchQuant'])

        return config

    @classmethod
    def load_test(cls):
        config = cls()

        config.copying_method = Copying.ELITISM_COPYING
        config.local_search_method = LocalSearch.PER_VARIABLE_LOCAL_SEARCH

        config.selection_method = Selection.ROULETTE_SELECTION
        config.crossover_method = Crossover.TWO_POINT_CROSSOVER
        config.mutation_method = Mutation.MULTI_BIT_INVERSION_MUTATION

        config.max_stagnation = 100

        config.population_size = 20
        config.top_selection_ratio = 0.2
        config.bottom_selection_ratio = 0.1
        config.mutation_chance = 0.01

        config.use_local_search = True
        config.local_search_step = 0.5
        config.local_search_quant = 10

        return config

    def update_from_args(self, args):
        if args.copying is not None:
            self.copying_method = Copying[args.copying + '_COPYING']

        if args.selection is not None:
            self.selection_method = Selection[args.selection + '_SELECTION']
        if args.crossover is not None:
            self.crossover_method = Crossover[args.crossover + '_CROSSOVER']
        if args.mutation is not None:
            self.mutation_method = Mutation[args.mutation + '_MUTATION']

        self.cost_budget = set_default(args.cost_budget, self.cost_budget)
        self.num_iterations = set_default(args.num_iterations, self.num_iterations)
        self.max_stagnation = set_default(args.max_stagnation, self.max_stagnation)

        self.population_size = set_default(args.population, self.population_size)
        self.top_selection_ratio = set_default(args.top, self.top_selection_ratio)
        self.bottom_selection_ratio = set_default(args.bottom, self.bottom_selection_ratio)
        self.mutation_chance = set_default(args.mutation_chance, self.mutation_chance)
