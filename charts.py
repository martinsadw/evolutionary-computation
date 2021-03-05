import pickle
import numpy as np
import matplotlib.pyplot as plt

import config
from fitness import Fitness

old_student_results = [Fitness.get_fitnessConcepts(student_id, config.concept_coverage.T) for student_id in range(config.num_students)]
student_results_before = sum(old_student_results)/config.num_students
print(f'student_results_before: {student_results_before}')



grasp_results = pickle.load( open( "results_grasp.pickle", "rb" ) )
grasp_concept_coverage = grasp_results["grasp_concept_coverage"]
grasp_progress = grasp_results["fitness_progress"]

grasp_student_results = [Fitness.get_fitnessConcepts(student_id, grasp_concept_coverage.T) for student_id in range(config.num_students)]


sa_results = pickle.load( open( "results_SA.pickle", "rb" ) )
sa_concept_coverage = sa_results["sa_concept_coverage"]
sa_progress = sa_results["fitness_progress"]

annealing_student_results = [Fitness.get_fitnessConcepts(student_id, sa_concept_coverage.T) for student_id in range(config.num_students)]



fig = plt.figure()
plt.bar(np.arange(config.num_students)-0.2, old_student_results,       width=0.2, align='center', label='None')
plt.bar(np.arange(config.num_students)    , annealing_student_results, width=0.2, align='center', label='SA')
plt.bar(np.arange(config.num_students)+0.2, grasp_student_results,     width=0.2, align='center', label='GRASP')
plt.xlabel('Students')
plt.ylabel('Objectives O1 + O4')
plt.legend(loc=1)
# # Save the figure as a PNG
plt.savefig('resultados_estudantes.pdf')
plt.show()

fig = plt.figure(figsize=(7, 3))

ax1 = plt.subplot(1, 2, 1)
ax1.plot(sa_progress,'g-')
ax1.legend(['Simulated Annealing'])
ax1.set_ylim(17,34)

ax2 = plt.subplot(1, 2, 2)
ax2.plot(grasp_progress,'b-')
ax2.legend(['GRASP'])
ax2.set_ylim(17,34)

fig.text(0.5, 0.01, 'Iterations', ha='center')
fig.text(0.04, 0.5, 'Objectives O1 + O4', va='center', rotation='vertical')
plt.savefig('iterations.pdf')