import numpy as np


def concepts_covered_function(individual, instance):
    objectives = instance.objectives
    concepts_materials = instance.concepts_materials
    missing_concepts_coeficient = instance.missing_concepts_coeficient

    covered_concepts = np.any(concepts_materials[:, individual], axis=1)
    over_covered_test = ~objectives & covered_concepts
    under_covered_test = objectives & ~covered_concepts

    # print("Conceitos adicionais: {}".format(over_covered_test.sum()))
    # print("Conceitos não cobertos: {}".format(under_covered_test.sum()))

    return over_covered_test.sum() + missing_concepts_coeficient * under_covered_test.sum()


# TODO(andre:2018-05-09): Decidir o que fazer quando um material nao ensina
# nenhum conceito nos objetivos do aluno
# TODO(andre:2018-05-09): Decidir o que fazer quando nenhum dos objetivos do
# aluno sao ensinados pelos materiais escolhidos
def difficulty_function(individual, instance):
    objectives = instance.objectives
    concepts_materials = instance.concepts_materials
    student_abilities = instance.student_abilities
    materials_difficulty = instance.materials_difficulty

    if (objectives.sum() == 0):
        return 0

    # print(objectives)
    # print(individual)
    # print(concepts_materials)
    # print(materials_difficulty)
    # print(student_abilities)

    selected_concepts_ability = student_abilities[objectives]
    selected_materials_difficulty = materials_difficulty[individual]
    selected_concepts_materials = concepts_materials[objectives, :][:, individual]

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
    # print(type(student_materials_difficulty.mean()))

    mean_student_materials_difficulty = student_materials_difficulty.mean()
    # Impede que a função retorne um maskedContant nos casos em que nenhum
    # material cobre conceitos dos objetivos do aluno
    if not isinstance(mean_student_materials_difficulty, float):
        # print("Nenhum objetivo coberto")
        mean_student_materials_difficulty = 0

    return mean_student_materials_difficulty


def total_time_function(individual, instance):
    estimated_time = instance.estimated_time
    duration_min = instance.duration_min
    duration_max = instance.duration_max

    masked_estimated_time = np.ma.array(estimated_time, mask=~individual)

    total_time = masked_estimated_time.sum()

    return max(duration_min - total_time, 0) + max(0, total_time - duration_max)


def materials_balancing_function(individual, instance):
    objectives = instance.objectives
    concepts_materials = instance.concepts_materials

    selected_concepts_materials = concepts_materials[objectives, :][:, individual]
    mean_concepts_per_objective = selected_concepts_materials.sum() / objectives.sum()

    materials_per_concepts = selected_concepts_materials.sum(axis=1)

    distance_from_mean = np.abs(materials_per_concepts - mean_concepts_per_objective)

    # print(selected_concepts_materials)
    # print(materials_per_concepts)
    # print(distance_from_mean)
    # print(mean_concepts_per_objective)

    return distance_from_mean.sum()


def learning_style_function(individual, instance):
    materials_active_reflexive = instance.materials_active_reflexive
    materials_sensory_intuitive = instance.materials_sensory_intuitive
    materials_visual_verbal = instance.materials_visual_verbal
    materials_sequential_global = instance.materials_sequential_global

    student_active_reflexive = instance.student_active_reflexive
    student_sensory_intuitive = instance.student_sensory_intuitive
    student_visual_verbal = instance.student_visual_verbal
    student_sequential_global = instance.student_sequential_global

    selected_active_reflexive = materials_active_reflexive[individual]
    selected_sensory_intuitive = materials_sensory_intuitive[individual]
    selected_visual_verbal = materials_visual_verbal[individual]
    selected_sequential_global = materials_sequential_global[individual]

    signal_active_reflexive = np.sign(selected_active_reflexive)
    signal_sensory_intuitive = np.sign(selected_sensory_intuitive)
    signal_visual_verbal = np.sign(selected_visual_verbal)
    signal_sequential_global = np.sign(selected_sequential_global)

    objective_active_reflexive = np.abs(3 * signal_active_reflexive - student_active_reflexive).mean()
    objective_sensory_intuitive = np.abs(3 * signal_sensory_intuitive - student_sensory_intuitive).mean()
    objective_visual_verbal = np.abs(3 * signal_visual_verbal - student_visual_verbal).mean()
    objective_sequential_global = np.abs(3 * signal_sequential_global - student_sequential_global).mean()

    return (objective_active_reflexive + objective_sensory_intuitive + objective_visual_verbal + objective_sequential_global) / 4
