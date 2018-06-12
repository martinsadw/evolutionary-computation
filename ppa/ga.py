import numpy as np
import random

from objective import fitness, fitness_population
from config import get_config_ga
from instance import Instance, print_instance


# TODO(felipe:2018-06-04): Adicionar outros métodos de crossover além do two-point
def crossover(individuals):
    cut_point1 = random.randint(0, individuals[0].size - 1)
    cut_point2 = random.randint(0, individuals[0].size - 1)

    while cut_point2 == cut_point1:
        if individuals[0].size == 1:
            break

        cut_point2 = random.randint(0, individuals[0].size - 1)

    if cut_point1 > cut_point2:
        cut_point1, cut_point2 = cut_point2, cut_point1

    new_individual = np.empty(individuals[0])

    for i in range(0, cut_point1):
        new_individual[i] = individuals[0]

    for i in range(cut_point1, cut_point2):
        new_individual[i] = individuals[1]

    for i in range(cut_point2, individuals[0].size):
        new_individual[i] = individuals[0]

    return new_individual


instance_test = Instance.load_from_file("../instance_files/config.txt")
print_instance(instance_test)
print("")
config = get_config_ga()

population_size = config['population_size']

population = np.random.randint(2, size=(population_size, instance_test.num_materials), dtype=bool)

selection_quant = 2

for generation in range(config['num_generations']):
    pass
