import numpy as np

from acs.objective import reduce_objectives
from utils.multiobjective import sort_nondominated
from read.algorithm import open_results, get_results_name, get_results_best_all_objectives


'''
Gerar o ponto de referencia para o hipervolume
    Para cada (instancia, estudante)
    Pior valor obtido entre todo mundo para cada objetivo

Gerar a melhor frente de pareto
    Para cada (instancia, estudante)
    Conjunto de individuos não dominados entre todas as soluções
'''

# return = {(instance_name, num_objectives): {worst_point, nondominated_population}}
# worst_point = students[(objectives)]
# nondominated_population = students[(individual, objectives)]
def get_instances_extremes(instances_results_name, extremes=None):
    if extremes is None:
        extremes = dict()

    num_objectives_list = [2, 3, 4, 5]

    for (instance_name, results_name_list) in instances_results_name.items():
        # worst_point[(instance_name, 5)] = None  # students[(num_objectives)]
        # nondominated_population[(instance_name, 5)] = None  # students[(num_individuals, num_objectives)]
        for results_name_info in results_name_list:
            results_name = get_results_name(*results_name_info)
            results = open_results(results_name)
            # (repetitions, students, individuals, MAX_OBJECTIVES)
            best_population = get_results_best_all_objectives(results)

            # print('instance_name:', instance_name)
            # print('results_name_info:', results_name_info)
            # print('results_name:', results_name)

            num_students = best_population.shape[1]
            num_individuals = best_population.shape[2]
            num_objectives = best_population.shape[3]

            for num_objectives in num_objectives_list:
                if (instance_name, num_objectives) not in extremes:
                    extremes[(instance_name, num_objectives)] = {
                        'worst_point': [None] * num_students,
                        'nondominated_population': [None] * num_students,
                    }

                instance_extremes = extremes[(instance_name, num_objectives)]
                for i in range(num_students):
                    # (repetitions, individuals, MAX_OBJECTIVES)
                    problem_best_population = best_population[:, i, :, :]
                    # (repetitions * individuals, MAX_OBJECTIVES)
                    problem_best_population = problem_best_population.reshape(problem_best_population.shape[0] * problem_best_population.shape[1], problem_best_population.shape[2])
                    # (repetitions * individuals, num_objectives)
                    problem_best_population = np.apply_along_axis(reduce_objectives, 1, problem_best_population, num_objectives)

                    instance_extremes['worst_point'][i] = get_worst_point(problem_best_population, base=instance_extremes['worst_point'][i])
                    instance_extremes['nondominated_population'][i] = get_nondominated_population(problem_best_population, base=instance_extremes['nondominated_population'][i])

    return extremes


# population = (individuals, objectives)
# return = (objectives)
def get_worst_point(population, base=None):
    worst = np.amax(population, axis=0)

    if base is not None:
        worst = np.maximum(worst, base)

    return worst


# population = (individuals, objectives)
# return = (individuals, objectives)
def get_nondominated_population(population, base=None):
    if base is not None:
        population = np.concatenate((population, base), axis=0)

    nondominated_index = sort_nondominated(population, first_front_only=True, include_repetition=False, sign=-1)[0]
    nondominated_population = population[nondominated_index]

    return nondominated_population
