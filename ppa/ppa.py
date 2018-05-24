# import random
import numpy as np

from objective import concepts_covered_function, difficulty_function, total_time_function, materials_balancing_function, learning_style_function
from config import get_config
from instance import Instance
# from roulette import Roulette


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


def fitness(individual, instance):
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

    print("Materiais do aluno:")
    print(individual)
    print("Penalidades: [{}, {}, {}, {}, {}] = {}".format(
        concepts_covered_objective,
        difficulty_objective,
        total_time_objective,
        materials_balancing_objective,
        learning_style_objective,
        sum_objective))
    print("")

    return sum_objective


#########################################

instance_test = Instance.load_from_file("../instance_files/config.txt")
# instance_test = Instance.load_test()
# instance = get_test_instance()
print_instance(instance_test)
config = get_config()

population_size = config['population_size']

population = np.random.randint(2, size=(population_size, instance_test.num_materials), dtype=bool)

survival_value = np.ones(population_size)
for i in range(population_size):
    # Calcula o valor de sobrevivencia do individuos i
    survival_value[i] = fitness(population[i], instance_test)

sorted_indices = np.argsort(survival_value)
population = population[sorted_indices]
survival_value = survival_value[sorted_indices]

population_distance = np.zeros((population_size, population_size))
survival_ratio = np.zeros((population_size, population_size))
for i in range(population_size):
    for j in range(population_size):
        population_distance[i, j] = hamming_distance(population[i], population[j]) / instance_test.num_materials
        survival_ratio[i, j] = survival_value[i] / survival_value[j]

follow_chance = (2 - config['follow_distance_parameter'] * population_distance - config['follow_survival_parameter'] * survival_ratio) / 2

follow_mask = np.random.randint(2, size=(population_size), dtype=bool)

num_steps = config['max_steps'] * np.random.rand(population_size) / np.exp(config['steps_distance_parameter'] * population_distance[:, -1])

# print(population)
# print(population_distance)
# print(survival_ratio)
# print(follow_chance)
# print(follow_chance[0])
# roulette = Roulette(follow_chance[0].tolist())
# results = [0] * population_size
# for i in range(1000):
#     results[roulette.spin()] += 1
#
# for i in range(population_size):
#     print(results[i])
