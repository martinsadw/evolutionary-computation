import pickle
from pprint import pprint

import numpy as np


# Compares the solution obtained by GA with the best solution obtained by NSGA
# for every pair (repetition, student)


################################################################################
## Loading #####################################################################
################################################################################

# (repetitions, students, iterations)
with open('results/algorithm_results/nsga_2_real.pickle', 'rb') as file:
    file_results_nsga = pickle.load(file)
    instance_nsga = file_results_nsga['info']['instance']
    instance_size = instance_nsga.num_materials
    results_nsga = file_results_nsga['data'][2]

# (repetitions, students, iterations, objectives)
with open('results/algorithm_results/ga_real.pickle', 'rb') as file:
    file_results_ga = pickle.load(file)
    instance_ga = file_results_ga['info']['instance']
    results_ga = file_results_ga['data'][2]

################################################################################
## Preparation #################################################################
################################################################################

# HACK(andre:2020-06-24): Fix the lack of order in the student list of NSGA results
nsga_sort = np.argsort(np.array(instance_nsga.learners_keys))
results_nsga = results_nsga[:, nsga_sort, :]

# Use only the last iteration
# (repetitions, students)
results_nsga = results_nsga[:, :, -1]
# (repetitions, students)
results_ga = results_ga[:, :, -1]

# Calculates when NSGA has better solutions than GA
# (repetitions, students)
nsga_comparison = (results_nsga < results_ga)

################################################################################
## Results #####################################################################
################################################################################

print('Dimensions: (repetitions, students)')
print('------------------------------------------------')
print('NSGA:', results_nsga.shape)
print('GA:', results_ga.shape)
print('Instance size: %d materials' % instance_size)
print('\n')

comparison_sum = nsga_comparison.sum()
comparison_total = nsga_comparison.size

np.set_printoptions(precision=3, suppress=True)
mean_ga = np.mean(results_ga, axis=0)
mean_nsga = np.mean(results_nsga, axis=0)
print('(NSGA - GA):')
print(mean_nsga - mean_ga)
print('Mean:', np.mean(mean_nsga - mean_ga))

print('\n')

print('NSGA wins (all): %3d / %d (%.2f%%)' % (comparison_sum, comparison_total, comparison_sum / comparison_total * 100))

num_students = results_nsga.shape[1]
print('\nNSGA wins per student (nondominated)')
for j in range(num_students):
    student_sum = nsga_comparison[:, j].sum()
    student_total = nsga_comparison[:, j].size

    print('Student %2d: %d / %d (%6.2f%%)' % ((j + 1), student_sum, student_total, student_sum / student_total * 100))
