# import random
import numpy as np

from objective import concepts_covered_function, difficulty_function, total_time_function, materials_balancing_function, learning_style_function
from config import get_config
from instance import Instance
from roulette import Roulette
from population_movement import move_population_roulette, move_population_direction, move_population_random, move_population_random_complement, move_population_local_search


# TODO(andre:2018-05-29): Mover essa funcao para um arquivo de utils
def hamming_distance(a, b):
    return np.sum(a != b)


def print_instance(instance):
    print("\nCobertura dos materiais:")
    print(instance.concepts_materials)

    print("\nObjetivos do aluno:")
    print(instance.objectives)

    print("\nHabilidades do aluno:")
    print(instance.student_abilities)

    print("\nDificuldades dos materiais:")
    print(instance.materials_difficulty)

    print("\nDuração dos materiais:")
    print(instance.estimated_time)

    print("\nDuração mínima:")
    print(instance.duration_min)

    print("\nDuração máxima:")
    print(instance.duration_max)

    print("\nEstilo dos materiais:")
    print("     Ativo | Reflexivo: {}".format(instance.materials_active_reflexive))
    print(" Sensorial | Intuitivo: {}".format(instance.materials_sensory_intuitive))
    print("    Visual | Verbal:    {}".format(instance.materials_visual_verbal))
    print("Sequencial | Global:    {}".format(instance.materials_sequential_global))

    print("\nEstilo do aluno:")
    print("     Ativo | Reflexivo: {}".format(instance.student_active_reflexive))
    print(" Sensorial | Intuitivo: {}".format(instance.student_sensory_intuitive))
    print("    Visual | Verbal:    {}".format(instance.student_visual_verbal))
    print("Sequencial | Global:    {}".format(instance.student_sequential_global))


def fitness(individual, instance, print_results=False):
    concepts_covered_objective = concepts_covered_function(individual, instance)
    difficulty_objective = difficulty_function(individual, instance)
    total_time_objective = total_time_function(individual, instance)
    materials_balancing_objective = materials_balancing_function(individual, instance)
    learning_style_objective = learning_style_function(individual, instance)

    sum_objective = (instance.concepts_covered_weight * concepts_covered_objective
                     + instance.difficulty_weight * difficulty_objective
                     + instance.total_time_weight * total_time_objective
                     + instance.materials_balancing_weight * materials_balancing_objective
                     + instance.learning_style_weight * learning_style_objective)

    if print_results:
        print("Materiais do aluno:")
        print(individual)
        print("Penalidades: [{}, {}, {}, {}, {}] = {}".format(
            concepts_covered_objective,
            difficulty_objective,
            total_time_objective,
            materials_balancing_objective,
            learning_style_objective,
            sum_objective))

    return sum_objective


def fitness_population(population, instance):
    population_size = population.shape[0]
    survival_values = np.empty(population_size)
    for i in range(population_size):
        # Calcula o valor de sobrevivencia do individuo i
        survival_values[i] = fitness(population[i], instance)

    return survival_values

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

    best_population = np.copy(new_population)
    best_survival_values = fitness_population(best_population, instance_test)
    for i in range(config['local_search_tries']):
        # print('-----------------------------' + str(i))
        num_steps = np.round(config['min_steps'] * np.random.rand(population_size))
        temp_population = move_population_random(new_population, num_steps, best_prey_mask)

        temp_survival_values = fitness_population(temp_population, instance_test)

        # print('Temp population:\n{}\n'.format(temp_population))
        # print('Temp survival values:\n{}\n'.format(temp_survival_values))

        better_survival_values = (temp_survival_values < best_survival_values)
        best_population = np.where(np.repeat(better_survival_values[:, np.newaxis], instance_test.num_materials, axis=1), temp_population, best_population)
        best_survival_values = np.where(better_survival_values, temp_survival_values, best_survival_values)
        # print('Partial best population:\n{}\n'.format(best_population))
        # print('Partial best survival values:\n{}\n'.format(best_survival_values))
    new_population[best_prey_mask] = best_population[best_prey_mask]

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
