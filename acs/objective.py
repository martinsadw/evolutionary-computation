import warnings

import numpy as np


INVALID_VALUE = 1000

def concepts_covered_function(individual, instance, student, timer):
    objectives = instance.objectives[student]
    concepts_materials = instance.concepts_materials
    missing_concepts_coeficient = instance.missing_concepts_coeficient
    timer.add_time("fitness_concept_start")

    # covered_concepts = np.any(concepts_materials & individual, axis=1)
    covered_concepts = np.sum(concepts_materials & individual, axis=1)

    timer.add_time("fitness_concept_lists1")
    # over_covered_test = ~objectives & covered_concepts
    # under_covered_test = objectives & ~covered_concepts
    over_covered_test = np.copy(covered_concepts)
    over_covered_test[objectives] = 0
    under_covered_test = objectives & (covered_concepts == 0)
    timer.add_time("fitness_concept_lists2")

    # print("Conceitos adicionais: {}".format(over_covered_test.sum()))
    # print("Conceitos não cobertos: {}".format(under_covered_test.sum()))

    result = over_covered_test.sum() + missing_concepts_coeficient * under_covered_test.sum()

    timer.add_time("fitness_concept_result")

    return result


def difficulty_function(individual, instance, student, timer):
    timer.add_time()
    objectives = instance.objectives[student]
    student_abilities = instance.student_abilities[student]
    concepts_materials = instance.concepts_materials
    materials_difficulty = instance.materials_difficulty

    if (objectives.sum() == 0):
        return 0

    # print(objectives)
    # print(individual)
    # print(concepts_materials)
    # print(materials_difficulty)
    # print(student_abilities)

    timer.add_time("fitness_difficulty_start")

    selected_concepts_ability = student_abilities[objectives]
    selected_materials_difficulty = materials_difficulty[individual]
    selected_concepts_materials = concepts_materials[objectives, :][:, individual]

    if selected_concepts_materials.size == 0:
        return INVALID_VALUE

    timer.add_time("fitness_difficulty_lists")

    tiled_student_ability = np.tile(selected_concepts_ability, (selected_materials_difficulty.shape[0], 1)).T
    timer.add_time("fitness_difficulty_tiled")
    masked_student_ability = np.ma.array(tiled_student_ability, mask=~selected_concepts_materials)
    timer.add_time("fitness_difficulty_masked")
    mean_student_ability = masked_student_ability.mean(axis=0)
    timer.add_time("fitness_difficulty_mean")

    student_materials_difficulty = np.abs(selected_materials_difficulty - mean_student_ability)

    timer.add_time("fitness_difficulty_abs")

    mean_student_materials_difficulty = student_materials_difficulty.mean()

    timer.add_time("fitness_difficulty_mean_difficulty")
    # Prevents the function to return maskedConstant in cases where no material
    # covers any student concepts
    # if not isinstance(mean_student_materials_difficulty, float):
    if mean_student_materials_difficulty is np.ma.masked:
        # print("Nenhum objetivo coberto")
        mean_student_materials_difficulty = INVALID_VALUE

    timer.add_time("fitness_difficulty_check")

    return mean_student_materials_difficulty


def total_time_function(individual, instance, student):
    duration_min = instance.duration_min[student]
    duration_max = instance.duration_max[student]
    estimated_time = instance.estimated_time

    masked_estimated_time = np.ma.array(estimated_time, mask=~individual)

    total_time = masked_estimated_time.sum()
    # Prevents the total time from materials to be maskedConstant when no
    # material has been selected for the learner
    if total_time is np.ma.masked:
        total_time = 0

    return max(duration_min - total_time, 0) + max(0, total_time - duration_max)


def materials_balancing_function(individual, instance, student):
    objectives = instance.objectives[student]
    concepts_materials = instance.concepts_materials

    selected_concepts_materials = concepts_materials[objectives, :][:, individual]
    mean_concepts_per_objective = selected_concepts_materials.sum() / objectives.sum()

    materials_per_concepts = selected_concepts_materials.sum(axis=1)

    distance_from_mean = np.abs(materials_per_concepts - mean_concepts_per_objective)

    # print(selected_concepts_materials)
    # print(materials_per_concepts)
    # print(distance_from_mean)
    # print(mean_concepts_per_objective)

    # print(materials_per_concepts)
    # print(mean_concepts_per_objective)

    return distance_from_mean.sum()


def learning_style_function(individual, instance, student):
    student_active_reflexive = instance.student_active_reflexive[student]
    student_sensory_intuitive = instance.student_sensory_intuitive[student]
    student_visual_verbal = instance.student_visual_verbal[student]
    student_sequential_global = instance.student_sequential_global[student]

    materials_active_reflexive = instance.materials_active_reflexive
    materials_sensory_intuitive = instance.materials_sensory_intuitive
    materials_visual_verbal = instance.materials_visual_verbal
    materials_sequential_global = instance.materials_sequential_global

    selected_active_reflexive = materials_active_reflexive[individual]
    selected_sensory_intuitive = materials_sensory_intuitive[individual]
    selected_visual_verbal = materials_visual_verbal[individual]
    selected_sequential_global = materials_sequential_global[individual]

    signal_active_reflexive = np.sign(selected_active_reflexive)
    signal_sensory_intuitive = np.sign(selected_sensory_intuitive)
    signal_visual_verbal = np.sign(selected_visual_verbal)
    signal_sequential_global = np.sign(selected_sequential_global)

    with warnings.catch_warnings():
        warnings.filterwarnings("error")

        try:
            objective_active_reflexive = np.abs(3 * signal_active_reflexive - student_active_reflexive).mean()
        except RuntimeWarning:
            objective_active_reflexive = INVALID_VALUE

        try:
            objective_sensory_intuitive = np.abs(3 * signal_sensory_intuitive - student_sensory_intuitive).mean()
        except RuntimeWarning:
            objective_sensory_intuitive = INVALID_VALUE

        try:
            objective_visual_verbal = np.abs(3 * signal_visual_verbal - student_visual_verbal).mean()
        except RuntimeWarning:
            objective_visual_verbal = INVALID_VALUE

        try:
            objective_sequential_global = np.abs(3 * signal_sequential_global - student_sequential_global).mean()
        except RuntimeWarning:
            objective_sequential_global = INVALID_VALUE

    return (objective_active_reflexive + objective_sensory_intuitive + objective_visual_verbal + objective_sequential_global) / 4


def fitness(individual, instance, student, timer, print_results=False, data=None, **kwargs):
    timer.add_time()
    concepts_covered_objective = concepts_covered_function(individual, instance, student, timer)
    timer.add_time()
    difficulty_objective = difficulty_function(individual, instance, student, timer)
    timer.add_time()
    total_time_objective = total_time_function(individual, instance, student)
    timer.add_time("fitness_total_time")
    materials_balancing_objective = materials_balancing_function(individual, instance, student)
    timer.add_time("fitness_materials")
    learning_style_objective = learning_style_function(individual, instance, student)
    timer.add_time("fitness_learning_style")

    sum_objective = (instance.concepts_covered_weight * concepts_covered_objective
                     + instance.difficulty_weight * difficulty_objective
                     + instance.total_time_weight * total_time_objective
                     + instance.materials_balancing_weight * materials_balancing_objective
                     + instance.learning_style_weight * learning_style_objective)

    timer.add_time("fitness_sum")

    if data is not None:
        new_data = (instance.concepts_covered_weight * concepts_covered_objective,
                    instance.difficulty_weight * difficulty_objective,
                    instance.total_time_weight * total_time_objective,
                    instance.materials_balancing_weight * materials_balancing_objective,
                    instance.learning_style_weight * learning_style_objective)

        data.append(new_data)

    if print_results:
        print("Materiais do aluno:")
        print(individual)
        print("Penalidades: [{}, {}, {}, {}, {}] = {}".format(
            instance.concepts_covered_weight * concepts_covered_objective,
            instance.difficulty_weight * difficulty_objective,
            instance.total_time_weight * total_time_objective,
            instance.materials_balancing_weight * materials_balancing_objective,
            instance.learning_style_weight * learning_style_objective,
            sum_objective))

    return sum_objective


def fitness_population(population, instance, student, timer, print_results=False, data=None):
    population_size = population.shape[0]
    survival_values = np.empty(population_size)

    for i in range(population_size):
        # Calculates the survival value of individual i
        survival_values[i] = fitness(population[i], instance, student, timer, print_results, data)

    return survival_values

def multi_fitness(individual, instance, student, timer, print_results=False, data=None, num_objectives=5, **kwargs):
    concepts_covered_objective = concepts_covered_function(individual, instance, student, timer)
    difficulty_objective = difficulty_function(individual, instance, student, timer)
    total_time_objective = total_time_function(individual, instance, student)
    materials_balancing_objective = materials_balancing_function(individual, instance, student)
    learning_style_objective = learning_style_function(individual, instance, student)

    objective = (instance.concepts_covered_weight * concepts_covered_objective,
                 instance.difficulty_weight * difficulty_objective,
                 instance.total_time_weight * total_time_objective,
                 instance.materials_balancing_weight * materials_balancing_objective,
                 instance.learning_style_weight * learning_style_objective)

    if num_objectives == 1:
        objective = (objective[0] + objective[1] + objective[2] + objective[3] + objective[4],)
    if num_objectives == 2:
        objective = (objective[0],
                     objective[1] + objective[2] + objective[3] + objective[4])
    if num_objectives == 3:
        objective = (objective[0],
                     objective[1],
                     objective[2] + objective[3] + objective[4])
    if num_objectives == 4:
        objective = (objective[0],
                     objective[1],
                     objective[4],
                     objective[2] + objective[3])
    # if num_objectives == 5:
    #     pass

    if data is not None:
        data.append(objective)

    if print_results:
        print("Materiais do aluno:")
        print(individual)
        print("Penalidades: [{}, {}, {}, {}, {}] = {}".format(
            instance.concepts_covered_weight * concepts_covered_objective,
            instance.difficulty_weight * difficulty_objective,
            instance.total_time_weight * total_time_objective,
            instance.materials_balancing_weight * materials_balancing_objective,
            instance.learning_style_weight * learning_style_objective,
            sum_objective))

    return objective
