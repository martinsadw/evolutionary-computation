from ga_copying import *
from ga_local_search import *
from ga_selection import *
from ga_crossover import *
from ga_mutation import *
from gene import *

# ELITISM_COPYING
# PERMISSIVE_COPYING
# NO_COPYING

# SINGLE_POINT_CROSSOVER
# TWO_POINT_CROSSOVER
# THREE_PARENT_CROSSOVER
# UNIFORM_CROSSOVER
# DECIMAL_CROSSOVER

# RANDOM_SELECTION
# ROULETTE_SELECTION


NUM_ITERATIONS = 1
OUTPUT_FILENAME = "gh.txt"


def get_config():
    config = {}

    config['copying_method'] = ELITISM_COPYING
    config['local_search_method'] = PER_VARIABLE_LOCAL_SEARCH

    config['selection_method'] = ROULETTE_SELECTION
    config['crossover_method'] = TWO_POINT_CROSSOVER
    config['mutation_method'] = BIT_INVERSION_MUTATION

    config['population_size'] = 20
    config['num_generations'] = 100

    config['top_selection_ratio'] = 0.2
    config['bottom_selection_ratio'] = 0.1
    config['mutation_chance'] = 0.01

    config['use_local_search'] = True
    config['local_search_step'] = 0.5
    config['local_search_quant'] = 10

    return config
