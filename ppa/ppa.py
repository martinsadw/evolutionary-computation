import random
import numpy as np

from ppa_material import *
from ppa_concepts import *


def concepts_covered_objective(objectives, materials, concepts_materials, missing_concepts_coeficient):
    covered_concepts = np.any(concepts_materials[:, materials], axis=1)
    over_covered_test = ~objectives & covered_concepts
    under_covered_test = objectives & ~covered_concepts

    # print("Conceitos adicionais: {}".format(over_covered_test.sum()))
    # print("Conceitos não cobertos: {}".format(under_covered_test.sum()))

    return over_covered_test.sum() + missing_concepts_coeficient * under_covered_test.sum()


# TODO(andre:2018-05-09): Decidir o que fazer quando um material nao ensina
# nenhum conceito nos objetivos do aluno

def difficulty_objective(objectives, materials, concepts_materials, student_ability, materials_difficulty):
    if (objectives.sum() == 0):
        return 0

    # print("===============================")
    # print("==Difficulty===================")
    # print(objectives)
    # print(materials)
    # print(concepts_materials)
    # print(materials_difficulty)
    # print(student_ability)

    selected_concepts_ability = student_ability[objectives]
    selected_materials_difficulty = materials_difficulty[materials]
    selected_concepts_materials = concepts_materials[objectives,:][:, materials]

    tiled_student_ability = np.tile(selected_concepts_ability, (selected_materials_difficulty.shape[0], 1)).T
    masked_student_ability = np.ma.array(tiled_student_ability, mask=~selected_concepts_materials)
    mean_student_ability = masked_student_ability.mean(axis=0)
    # mean_student_ability = masked_student_ability.mean(axis=0).filled(0)

    student_materials_difficulty = np.abs(selected_materials_difficulty - mean_student_ability)

    # print(selected_concepts_ability)
    # print(selected_materials_difficulty)
    # print(selected_concepts_materials)
    # print(mean_student_ability)
    # print(student_materials_difficulty)
    # print(student_materials_difficulty.mean())

    return student_materials_difficulty.mean()


def total_time_objective(materials, estimated_time, duration_min, duration_max):
    masked_estimated_time = np.ma.array(estimated_time, mask=~materials)

    total_time = masked_estimated_time.sum()

    return max(duration_min - total_time, 0) + max(0, total_time - duration_max)


def materials_balancing_objective(objectives, materials, concepts_materials):
    selected_concepts_materials = concepts_materials[objectives,:][:, materials]
    mean_concepts_per_objective = selected_concepts_materials.sum() / objectives.sum()

    materials_per_concepts = selected_concepts_materials.sum(axis=1)

    distance_from_mean = np.abs(materials_per_concepts - mean_concepts_per_objective)

    # print(selected_concepts_materials)
    # print(materials_per_concepts)
    # print(distance_from_mean)
    # print(mean_concepts_per_objective)

    return distance_from_mean.sum()


def learning_style_objective(materials,
                             materials_active_reflexive, materials_sensory_intuitive, materials_visual_verbal, materials_sequential_global,
                             student_active_reflexive, student_sensory_intuitive, student_visual_verbal, student_sequential_global):

    selected_active_reflexive = materials_active_reflexive[materials]
    selected_sensory_intuitive = materials_sensory_intuitive[materials]
    selected_visual_verbal = materials_visual_verbal[materials]
    selected_sequential_global = materials_sequential_global[materials]

    signal_active_reflexive = np.sign(selected_active_reflexive)
    signal_sensory_intuitive = np.sign(selected_sensory_intuitive)
    signal_visual_verbal = np.sign(selected_visual_verbal)
    signal_sequential_global = np.sign(selected_sequential_global)

    objective_active_reflexive = np.abs(3 * signal_active_reflexive - student_active_reflexive).mean()
    objective_sensory_intuitive = np.abs(3 * signal_sensory_intuitive - student_sensory_intuitive).mean()
    objective_visual_verbal = np.abs(3 * signal_visual_verbal - student_visual_verbal).mean()
    objective_sequential_global = np.abs(3 * signal_sequential_global - student_sequential_global).mean()

    return (objective_active_reflexive + objective_sensory_intuitive + objective_visual_verbal + objective_sequential_global) / 4

def hamming_distance(a, b):
    return np.sum(a != b)


concepts_list = create_concepts_list()
materials_list = create_materials_list()

num_concepts = len(concepts_list)
num_materials = len(materials_list)
population_size = 5

ability = np.zeros(num_concepts)
objectives = np.zeros(num_concepts, dtype=bool)

duration_min = 0
duration_max = 50
student_active_reflexive = 3
student_sensory_intuitive = 2
student_visual_verbal = -1
student_sequential_global = -2

difficulty = np.zeros(num_materials)
concepts_materials = np.zeros((num_concepts, num_materials), dtype=bool)
estimated_time = np.zeros(num_materials)
materials_active_reflexive = np.zeros(num_materials)
materials_sensory_intuitive = np.zeros(num_materials)
materials_visual_verbal = np.zeros(num_materials)
materials_sequential_global = np.zeros(num_materials)

population = np.random.randint(2, size=(population_size, num_materials), dtype=bool)
# print(population)

# distance = hamming_distance(population[0], population[1])
# print(distance)

# cover = concepts_covered_objective(objectives, population[0], concepts_materials)
# print(cover)

# difficulty_objective(objectives, population[0], concepts_materials, difficulty, ability)

concepts_materials_test = np.array([
    [0, 0, 0, 0, 1, 1, 0],
    [1, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 1],
], dtype=bool)

objectives_test = np.array([0, 1, 1, 1, 0], dtype=bool)
materials_test = np.array([1, 0, 1, 0, 1, 0, 0], dtype=bool)

ability_test = np.array([0.5, 0.3, 0.1, 0.2, 0.9])
difficulty_test = np.array([0.8, 0.7, 0.8, 0.3, 0.5, 0.1, 0.3])

estimated_time_test = np.array([20, 20, 30, 45, 10, 50, 35])

duration_min_test = 0
duration_max_test = 50

materials_active_reflexive_test = np.array([2, 1, -2, -4, 3, 0, -1])
materials_sensory_intuitive_test = np.array([1, 4, 3, -2, -3, 0, 2])
materials_visual_verbal_test = np.array([2, -1, -1, 5, 0, 0, 3])
materials_sequential_global_test = np.array([-3, -2, 2, 1, 3, 3, -1])

student_active_reflexive_test = 3
student_sensory_intuitive_test = 2
student_visual_verbal_test = -1
student_sequential_global_test = -2

print("\nCobertura dos materiais:")
print(concepts_materials_test)

print("\nObjetivos do aluno:")
print(objectives_test)

print("\nMateriais do aluno:")
print(materials_test)

print("\nHabilidades do aluno:")
print(ability_test)

print("\nDificuldades dos materiais:")
print(difficulty_test)

print("\nDuração dos materiais:")
print(estimated_time_test)

print("\nDuração mínima:")
print(duration_min_test)

print("\nDuração máxima:")
print(duration_max_test)

print("\nEstilo dos materiais:")
print("     Ativo | Reflexivo: {}".format(materials_active_reflexive_test))
print(" Sensorial | Intuitivo: {}".format(materials_sensory_intuitive_test))
print("    Visual | Verbal:    {}".format(materials_visual_verbal_test))
print("Sequencial | Global:    {}".format(materials_sequential_global_test))

print("\nEstilo do aluno:")
print("     Ativo | Reflexivo: {}".format(student_active_reflexive_test))
print(" Sensorial | Intuitivo: {}".format(student_sensory_intuitive_test))
print("    Visual | Verbal:    {}".format(student_visual_verbal_test))
print("Sequencial | Global:    {}".format(student_sequential_global_test))

print("")

concepts_covered_objective_test = concepts_covered_objective(objectives_test, materials_test, concepts_materials_test, 2)
print("Penalidade por cobertura de conceitos: {}".format(concepts_covered_objective_test))

difficulty_objective_test = difficulty_objective(objectives_test, materials_test, concepts_materials_test, ability_test, difficulty_test)
print("Penalidade por dificuldade: {}".format(difficulty_objective_test))

total_time_objective_test = total_time_objective(materials_test, estimated_time_test, duration_min_test, duration_max_test)
print("Penalidade por tempo total: {}".format(total_time_objective_test))

materials_balancing_objective_test = materials_balancing_objective(objectives_test, materials_test, concepts_materials_test)
print("Penalidade por desbalanceamento: {}".format(materials_balancing_objective_test))

learning_style_objective_test = learning_style_objective(materials_test,
                                                         materials_active_reflexive_test, materials_active_reflexive_test, materials_visual_verbal_test, materials_sequential_global_test,
                                                         student_active_reflexive_test, student_sensory_intuitive_test, student_visual_verbal_test, student_sequential_global_test)
print("Penalidade por estilo de aprendizado: {}".format(learning_style_objective_test))

print("\nPenalidade total: {}".format(1 * concepts_covered_objective_test +
                                      1 * difficulty_objective_test +
                                      1 * total_time_objective_test +
                                      1 * materials_balancing_objective_test +
                                      1 * learning_style_objective_test))
