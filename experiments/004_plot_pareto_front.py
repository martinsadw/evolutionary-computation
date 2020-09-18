import os
from pprint import pprint

import numpy as np

from pymoo.factory import get_problem
from pymoo.visualization.scatter import Scatter

from acs.objective import reduce_objectives
from read.algorithm import create_results_name_list, get_results_name, open_results, get_results_best_all_objectives, get_results_best_n_objectives
from read.extremes import create_extremes_name_list, get_extremes_name, open_extremes, get_extremes_worst_point, get_extremes_nondominated_population


# Plots the graphs comparing each result with the pareto front


colors = {
    'pareto': '#1f77b4',
    'ga': '#ff7f0e',
    'nsga_ii_2': '#2ca02c',
    'nsga_ii_3': '#d62728',
    'worst': '#9467bd',
}

file_format = 'png'
results_path = 'results/2020-09-17 - Frente de pareto'

instances = ['andre_50', 'andre_300', 'andre_1000', 'real']
comparison_num_objectives = [2, 3, 5]

for instance in instances:
    os.makedirs(os.path.join(results_path, instance, '2 objectives'), exist_ok=True)
    os.makedirs(os.path.join(results_path, instance, '3 objectives'), exist_ok=True)
    os.makedirs(os.path.join(results_path, instance, '5 objectives'), exist_ok=True)

worst_point = {}
nondominated_population = {}

print('Reading data')
print('============\n')
extremes_name_list = create_extremes_name_list(instances, comparison_num_objectives)
for extremes_name_info in extremes_name_list:
    extremes_name = get_extremes_name(*extremes_name_info)
    extremes = open_extremes(extremes_name)
    worst_point[extremes_name_info] = get_extremes_worst_point(extremes)
    nondominated_population[extremes_name_info] = get_extremes_nondominated_population(extremes)

instances_results = {}
instances_results_name = create_results_name_list(instances, ['ga'], ['nsga_ii'], [2, 3])
for (instance_name, results_name_list) in instances_results_name.items():
    instances_results[instance_name] = {}
    for results_name_info in results_name_list:
        results_name = get_results_name(*results_name_info)
        results = open_results(results_name)

        num_objectives = results_name_info[2]
        if num_objectives is None:
            algorithm_name = results_name_info[0]
        else:
            algorithm_name = '%s_%d' % (results_name_info[0], num_objectives)

        # (repetitions, students, individuals, MAX_OBJECTIVES)
        best_population = get_results_best_all_objectives(results)
        num_students = best_population.shape[1]

        instances_results[instance_name][algorithm_name] = [None] * num_students
        for i in range(num_students):
            problem_best_population = best_population[:, i, :, :]
            problem_best_population = problem_best_population.reshape(problem_best_population.shape[0] * problem_best_population.shape[1], problem_best_population.shape[2])
            instances_results[instance_name][algorithm_name][i] = problem_best_population

print('Generating graphs')
print('=================\n')

for (instance_name, algorithm_results) in instances_results.items():
    print(instance_name)
    print('---------\n')
    for n in comparison_num_objectives:
        print('%d objectives' % n)
        num_students = len(algorithm_results['ga'])
        for i in range(num_students):
            problem_worst_point = worst_point[(instance_name, n)][i]
            pareto_front = nondominated_population[(instance_name, n)][i]

            gd = get_performance_indicator("gd", pareto_front)

            filepath = os.path.join(results_path, instance_name, '%d objectives' % n, '%d.%s' % (i, file_format))

            legend = True if n <= 3 else False
            # scatter = Scatter(legend=legend)
            # scatter.add(pareto_front, label='Pareto-front', s=60, color=colors['pareto'])

            size = 30
            for algorithm_name in algorithm_results.keys():
                problem_best_population = np.apply_along_axis(reduce_objectives, 1, algorithm_results[algorithm_name][i], n)
                # scatter.add(problem_best_population, label=algorithm_name, s=size, color=colors[algorithm_name])
                size /= 2

            # scatter.add(problem_worst_point, label="Worst", s=100, color=colors['worst'])
            # scatter.save(filepath)




# print('Comparing GA with NSGA-II using two objetives')
# print('=============================================\n')
# instances_results_name = create_results_name_list(instances, ['ga'], ['nsga_ii'], [2, 3])
# for (instance_name, results_name_list) in instances_results_name.items():
#     print(instance_name)
#     print('---------\n')
#     for results_name_info in results_name_list:
#         print(results_name_info)
#         results_name = get_results_name(*results_name_info)
#         results = open_results(results_name)
#
#         algorithm_name = results_name_info[0]
#         num_objectives = results_name_info[2]
#
#         # (repetitions, students, individuals, num_objectives)
#         best_population = get_results_best_n_objectives(results, 2)
#         num_students = best_population.shape[1]
#
#         for i in range(num_students):
#             problem_best_population = best_population[:, i, :, :]
#             problem_best_population = problem_best_population.reshape(problem_best_population.shape[0] * problem_best_population.shape[1], problem_best_population.shape[2])
#
#             pareto_front = nondominated_population[(instance_name, 2)][i]
#             problem_worst_point = worst_point[(instance_name, 2)][i]
#
#             if num_objectives is None:
#                 filepath = os.path.join(results_path, instance_name, '2 objectives', algorithm_name, '%d.%s' % (i, file_format))
#             else:
#                 filepath = os.path.join(results_path, instance_name, '2 objectives', '%s_%d' % (algorithm_name, num_objectives), '%d.%s' % (i, file_format))
#
#             scatter = Scatter(legend=True)
#             scatter.add(pareto_front, label="Pareto-front")
#             scatter.add(problem_best_population, label="Result", s=8)
#             scatter.add(problem_worst_point, label="Worst", s=100)
#             scatter.save(filepath)
#     print('')
#
# assert(False)
#
# print('Comparing GA with NSGA-II using three objetives')
# print('===============================================\n')
# instances_results_name = create_results_name_list(instances, ['ga'], ['nsga_ii'], [2, 3])
# for (instance_name, results_name_list) in instances_results_name.items():
#     print(instance_name)
#     print('---------\n')
#     for results_name_info in results_name_list:
#         print(results_name_info)
#         results_name = get_results_name(*results_name_info)
#         results = open_results(results_name)
#
#         best_population = get_results_best_n_objectives(results, 3)
#         num_students = best_population.shape[1]
#
#         for i in range(num_students):
#             problem_best_population = best_population[:, i, :, :]
#             problem_best_population = problem_best_population.reshape(problem_best_population.shape[0] * problem_best_population.shape[1], problem_best_population.shape[2])
#
#             pareto_front = nondominated_population[(instance_name, 3)][i]
#             problem_worst_point = worst_point[(instance_name, 3)][i]
#             # Scatter(legend=True).add(pareto_front, label="Pareto-front").add(problem_best_population, label="Result", s=10).show()
#             # if num_objectives is None:
#             #     filename = '%s_%s_%d.%s' % (instance_name, algorithm_name, i, results_format)
#             # else:
#             #     filename = '%s_%s_%d_%d.%s' % (instance_name, algorithm_name, num_objectives, i, results_format)
#             # Scatter(legend=True).add(pareto_front, label="Pareto-front").add(problem_best_population, label="Result", s=8).save(os.path.join(results_path, '2', filename))
#     print('')
#
# print('Comparing GA with NSGA-II using five objetives')
# print('==============================================\n')
# instances_results_name = create_results_name_list(instances, ['ga'], ['nsga_ii'], [2, 3])
# for (instance_name, results_name_list) in instances_results_name.items():
#     print(instance_name)
#     print('---------\n')
#     for results_name_info in results_name_list:
#         print(results_name_info)
#         results_name = get_results_name(*results_name_info)
#         results = open_results(results_name)
#
#         best_population = get_results_best_n_objectives(results, 5)
#         num_students = best_population.shape[1]
#
#         for i in range(num_students):
#             problem_best_population = best_population[:, i, :, :]
#             problem_best_population = problem_best_population.reshape(problem_best_population.shape[0] * problem_best_population.shape[1], problem_best_population.shape[2])
#
#             pareto_front = nondominated_population[(instance_name, 5)][i]
#             problem_worst_point = worst_point[(instance_name, 5)][i]
#     print('')
#
# assert(False)