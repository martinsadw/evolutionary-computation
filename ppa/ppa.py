# import random
import numpy as np

from objective import fitness, fitness_population
from config import get_config
from instance import Instance, print_instance
from roulette import Roulette
from population_movement import move_population_roulette, move_population_direction, move_population_random, move_population_random_complement, move_population_local_search


# TODO(andre:2018-05-29): Mover essa funcao para um arquivo de utils
def hamming_distance(a, b):
    return np.sum(a != b)


#########################################

instance_test = Instance.load_from_file("../instance_files/config.txt")
# instance_test = Instance.load_test()
# instance = get_test_instance()
print_instance(instance_test)
print("")
config = get_config()

population_size = config['population_size']

population = np.random.randint(2, size=(population_size, instance_test.num_materials), dtype=bool)

for iteration in range(config['num_iterations']):
    # print('==========================' + str(iteration))
    survival_values = fitness_population(population, instance_test)
    sorted_indices = np.argsort(survival_values)
    population = population[sorted_indices]
    survival_values = survival_values[sorted_indices]
    # print('Survival values:\n{}\n'.format(survival_values))

    new_population = np.copy(population)

    population_distance = np.empty((population_size, population_size))
    survival_ratio = np.empty((population_size, population_size))
    for i in range(population_size):
        for j in range(population_size):
            population_distance[i, j] = hamming_distance(population[j], population[i]) / instance_test.num_materials
            survival_ratio[i, j] = survival_values[j] / survival_values[i]
    follow_chance = (2 - config['follow_distance_parameter'] * population_distance - config['follow_survival_parameter'] * survival_ratio) / 2
    # TODO(andre:2018-05-29): A roleta não permite armazenar itens arbitrarios da
    # populacao. O funcionamento atual depende dos elementos utilizados serem sempre
    # os i primeiros elementos da populacao
    roulette_array = np.array([Roulette(follow_chance[i, :i].tolist()) for i in range(population_size)])

    # Cria as mascaras para separar os diferentes tipos de individuo
    best_prey_mask = np.zeros(population_size, dtype=bool)
    best_prey_mask[0] = True

    predator_mask = np.zeros(population_size, dtype=bool)
    predator_mask[-1] = True

    follow_mask = (np.random.rand(population_size) < config['follow_chance'])
    run_mask = ~follow_mask

    follow_mask[best_prey_mask] = False # Ignora as melhores presas
    follow_mask[predator_mask] = False # Ignora os predadores

    run_mask[best_prey_mask] = False # Ignora as melhores presas
    run_mask[predator_mask] = False # Ignora os predadores

    # print('Best prey mask: {}'.format(best_prey_mask))
    # print(' Predator mask: {}'.format(predator_mask))
    # print('   Follow mask: {}'.format(follow_mask))
    # print('      Run mask: {}'.format(run_mask))

    # TODO(andre:2018-05-28): Garantir que max_steps nunca é maior do que o numero de materiais
    num_steps = np.round(config['max_steps'] * np.random.rand(population_size) / np.exp(config['steps_distance_parameter'] * population_distance[:, -1]))
    new_population = move_population_roulette(new_population, num_steps, roulette_array, population, follow_mask)

    num_steps = np.round(config['min_steps'] * np.random.rand(population_size))
    new_population = move_population_random(new_population, num_steps, follow_mask)

    num_steps = np.round(config['max_steps'] * np.random.rand(population_size))
    new_population = move_population_random_complement(new_population, num_steps, population[-1], run_mask)

    new_population = move_population_local_search(new_population, best_prey_mask, config['min_steps'], config['local_search_tries'], instance_test)

    num_steps = np.round(config['max_steps'] * np.random.rand(population_size))
    new_population = move_population_random(new_population, num_steps, predator_mask)

    num_steps = np.round(config['min_steps'] * np.random.rand(population_size))
    worst_prey = np.repeat(population[-2][np.newaxis, :], population_size, axis=0)
    new_population = move_population_direction(new_population, num_steps, worst_prey, predator_mask)

    new_survival_values = fitness_population(new_population, instance_test)
    # print('Old population:\n{}\n'.format(population))
    # print('New population:\n{}\n'.format(new_population))
    # print('Comparison:\n{}\n'.format(population == new_population))
    # print('Old survival values:\n{}\n'.format(survival_values))
    # print('New survival values:\n{}\n'.format(new_survival_values))

    population = new_population

survival_values = fitness_population(population, instance_test)
sorted_indices = np.argsort(survival_values)
population = population[sorted_indices]
survival_values = survival_values[sorted_indices]

print('Population:\n{}\n'.format(population))
print('Survival values:\n{}\n'.format(survival_values))
print('a: {}\n'.format(fitness(np.array([True, False, False, False, False, False]), instance_test, True)))
print('b: {}\n'.format(fitness(np.array([False, False, False, False, True, False]), instance_test, True)))
print('c: {}\n'.format(fitness(np.array([True, True, True, True, True, True]), instance_test, True)))
print('d: {}\n'.format(fitness(np.array([False, False, False, False, False, False]), instance_test, True)))
