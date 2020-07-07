import pickle
from pprint import pprint

import numpy as np

from acs.objective import fitness, multi_fitness, reduce_objectives
from utils.multiobjective import dominates, sort_nondominated
from utils.timer import Timer


# Compares how many solution obtained by NSGA are dominated by the solution
# obtained by GA for every pair (repetition, student) considering all objectives


################################################################################
## Loading #####################################################################
################################################################################

# (repetitions, students, individuals, materials)
with open('results/algorithm_results/nsga_2_real.pickle', 'rb') as file:
    file_results_nsga = pickle.load(file)
    instance_nsga = file_results_nsga['info']['instance']
    instance_size = instance_nsga.num_materials
    selected_nsga = file_results_nsga['data'][0]

# (repetitions, students, materials)
# # (repetitions, students, iterations, objectives)
with open('results/algorithm_results/ga_real.pickle', 'rb') as file:
    file_results_ga = pickle.load(file)
    instance_ga = file_results_ga['info']['instance']
    selected_ga = file_results_ga['data'][0]

################################################################################
## Preparation #################################################################
################################################################################

num_repetitions = selected_nsga.shape[0]
num_students = selected_nsga.shape[1]
num_individuals = selected_nsga.shape[2]
num_objectives = 5

# Calculate the fitness value considering all objectives
# (repetitions, students, individuals, objectives)
timer = Timer()
instance_nsga.duration_max[:] = 3600
instance_ga.duration_max[:] = 3600
results_ga = np.empty((num_repetitions, num_students, 1, num_objectives))
results_nsga = np.empty((num_repetitions, num_students, num_individuals, num_objectives))
for i in range(num_repetitions):
    for j in range(num_students):
        results_ga[i, j, 0] = multi_fitness(selected_ga[i, j], instance_ga, j, timer)
        for k in range(num_individuals):
            results_nsga[i, j, k] = multi_fitness(selected_nsga[i, j, k], instance_nsga, j, timer)

# previous = True
# exclude = 4
#
# if previous:
#     for i in range(results_nsga.shape[3]):
#         if i != exclude:
#             results_nsga[:, :, :, i] = 0
#             results_ga[:, :, :, i] = 0
#     np.set_printoptions(precision=3, suppress=True)
#     print(results_ga[:, :, 0, exclude])
#     print(np.min(results_nsga[:, :, :, exclude], axis=2))
#     print()
#     print(results_ga[:, :, 0, exclude] - np.min(results_nsga[:, :, :, exclude], axis=2))

# Calculates NSGA nondominated individuals
# (repetitions, students, individuals)
nondominated_repetition_mask = np.zeros((num_repetitions, num_students, num_individuals), dtype=bool)
nondominated_mask = np.zeros((num_repetitions, num_students, num_individuals), dtype=bool)
for i in range(num_repetitions):
    for j in range(num_students):
        population = results_nsga[i, j]

        nondominated_repetition_population = sort_nondominated(population, first_front_only=True, include_repetition=True, sign=-1)[0]
        nondominated_repetition_mask[i, j, nondominated_repetition_population] = True

        nondominated_population = sort_nondominated(population, first_front_only=True, include_repetition=False, sign=-1)[0]
        nondominated_mask[i, j, nondominated_population] = True

# if not previous:
#     for i in range(results_nsga.shape[3]):
#         if i != exclude:
#             results_nsga[:, :, :, i] = 0
#             results_ga[:, :, :, i] = 0
#     np.set_printoptions(precision=3, suppress=True)
#     print(results_ga[:, :, 0, exclude])
#     print(np.mean(results_nsga[:, :, :, exclude], axis=2))
#     print()
#     print(results_ga[:, :, 0, exclude] - np.mean(results_nsga[:, :, :, exclude], axis=2))

# Calculates which individual are dominated by GA or by NSGA
# (repetitions, students, individuals)
repetition_nsga_dominates = np.zeros((num_repetitions, num_students, num_individuals), dtype=bool)
repetition_ga_dominates = np.zeros((num_repetitions, num_students, num_individuals), dtype=bool)
nsga_dominates = np.zeros((num_repetitions, num_students, num_individuals), dtype=bool)
ga_dominates = np.zeros((num_repetitions, num_students, num_individuals), dtype=bool)
for i in range(num_repetitions):
    for j in range(num_students):
        nondominated_repetition_population = nondominated_repetition_mask[i, j].nonzero()[0]
        nondominated_population = nondominated_mask[i, j].nonzero()[0]

        ga_result = results_ga[i, j, 0]

        for k in nondominated_repetition_population:
            nsga_result = results_nsga[i, j, k]
            if dominates(nsga_result, ga_result, sign=-1):
                repetition_nsga_dominates[i, j, k] = True
            if dominates(ga_result, nsga_result, sign=-1):
                repetition_ga_dominates[i, j, k] = True

        for k in nondominated_population:
            nsga_result = results_nsga[i, j, k]
            if dominates(nsga_result, ga_result, sign=-1):
                nsga_dominates[i, j, k] = True
            if dominates(ga_result, nsga_result, sign=-1):
                ga_dominates[i, j, k] = True

################################################################################
## Results #####################################################################
################################################################################

print('Dimensions: (repetitions, students, individuals, objectives)')
print('------------------------------------------------')
print('NSGA:', results_nsga.shape)
print('GA:', results_ga.shape)
print('Instance size: %d materials' % instance_size)
print('\n')

# With repetition
total_nond_rep = nondominated_repetition_mask.sum()
nsga_dom_rep = repetition_nsga_dominates.sum()
ga_dom_rep = repetition_ga_dominates.sum()
neither_rep = total_nond_rep - (nsga_dom_rep + ga_dom_rep)

neither_perc_rep = neither_rep / total_nond_rep * 100
nsga_perc_rep = nsga_dom_rep / total_nond_rep * 100
ga_perc_rep = ga_dom_rep / total_nond_rep * 100

# Without repetition
total_nond = nondominated_mask.sum()
nsga_dom = nsga_dominates.sum()
ga_dom = ga_dominates.sum()
neither = total_nond - (nsga_dom + ga_dom)

neither_perc = neither / total_nond * 100
nsga_perc = nsga_dom / total_nond * 100
ga_perc = ga_dom / total_nond * 100


print('Number of individuals: %d' % nondominated_mask.size)
print('     Dominates |       GA       |     Neither    |      NSGA      | Total ')
print('---------------+----------------+----------------+----------------+-------')
print('w/  repetition | %4d (%6.2f%%) | %4d (%6.2f%%) | %4d (%6.2f%%) | %5d' % (ga_dom_rep, ga_perc_rep, neither_rep, neither_perc_rep, nsga_dom_rep, nsga_perc_rep, total_nond_rep))
print('w/o repetition | %4d (%6.2f%%) | %4d (%6.2f%%) | %4d (%6.2f%%) | %5d' % (ga_dom, ga_perc, neither, neither_perc, nsga_dom, nsga_perc, total_nond))

print('\n')

print('GA dominates per student (w/o repetition)')
print('     Dominates |       GA       |     Neither    |      NSGA      | Total ')
print('---------------+----------------+----------------+----------------+-------')
for j in range(num_students):
    stud_total_nond = nondominated_mask[:, j, :].sum()
    stud_nsga_dom = nsga_dominates[:, j, :].sum()
    stud_ga_dom = ga_dominates[:, j, :].sum()
    stud_neither = stud_total_nond - (stud_nsga_dom + stud_ga_dom)

    stud_neither_perc = stud_neither / stud_total_nond * 100
    stud_nsga_perc = stud_nsga_dom / stud_total_nond * 100
    stud_ga_perc = stud_ga_dom / stud_total_nond * 100

    print('    Student %2d | %4d (%6.2f%%) | %4d (%6.2f%%) | %4d (%6.2f%%) | %5d' % ((j + 1), stud_ga_dom, stud_ga_perc, stud_neither, stud_neither_perc, stud_nsga_dom, stud_nsga_perc, stud_total_nond))

    # student_sum = ga_dominates[:, j, :].sum()
    # student_total = nondominated_mask[:, j, :].sum()

    # print('Student %2d: %3d / %3d (%6.2f%%)' % ((j + 1), student_sum, student_total, student_sum / student_total * 100))

# ga_nond = ga_dominates.sum()
# ga_nond_rep = repetition_ga_dominates.sum()
# total_nond = nondominated_mask.sum()
# total_nond_rep = nondominated_repetition_mask.sum()

# print('GA dominates (w/  repetition): %4d / %4d (%.2f%%)' % (ga_nond_rep, total_nond_rep, ga_nond_rep / total_nond_rep * 100))
# print('GA dominates (w/o repetition): %4d / %4d (%.2f%%)' % (ga_nond, total_nond, ga_nond / total_nond * 100))
