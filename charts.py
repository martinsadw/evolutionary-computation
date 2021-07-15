import pickle
import numpy as np
import matplotlib.pyplot as plt

import config
from fitness import Fitness

old_student_results = [Fitness.get_fitnessConcepts(student_id, config.concept_coverage.T) for student_id in range(config.num_students)]
student_results_before = sum(old_student_results)/config.num_students
print(f'student_results_before: {student_results_before}')



grasp_results = pickle.load( open( "results_grasp.pickle", "rb" ) )

#grasp_concept_coverage = grasp_results["grasp_concept_coverage"]
grasp_progress = grasp_results["fitness_progress"]
cost_grasp_progress = grasp_results["cost_progress"]

grasp_student_results = [Fitness.get_fitnessConcepts(student_id, grasp_concept_coverage.T) for student_id in range(config.num_students)]


sa_results = pickle.load( open( "results_SA.pickle", "rb" ) )
sa_concept_coverage = sa_results["sa_concept_coverage"]
sa_progress = sa_results["fitness_progress"]
cost_sa_progress = sa_results["cost_progress"]

annealing_student_results = [Fitness.get_fitnessConcepts(student_id, sa_concept_coverage.T) for student_id in range(config.num_students)]


fig = plt.figure()
ax = plt.subplot()

ax.plot(cost_grasp_progress,grasp_progress,'g-',label ="GRASP")
ax.plot(cost_sa_progress,sa_progress,'b-',label="Simulated Annealing")
plt.yticks(np.arange(16,34, 1.50))
ax.legend(loc = 0)
fig.text(0.5, 0.01, 'Computational cost', ha='center')
fig.text(0.01, 0.5, 'Objectives O1 + O4', va='center', rotation='vertical')
plt.savefig('teste_10k.png')



'''
fig = plt.figure()
plt.bar(np.arange(config.num_students)-0.2, old_student_results,       width=0.2, align='center', label='Baseline')
plt.bar(np.arange(config.num_students)    , annealing_student_results, width=0.2, align='center', label='SA')
plt.bar(np.arange(config.num_students)+0.2, grasp_student_results,     width=0.2, align='center', label='GRASP')
plt.xlabel('Students')
plt.ylabel('Objectives O1 + O4')
plt.legend(loc=1)
# # Save the figure as a PNG
plt.savefig('resultados_estudantes.pdf')
plt.show()


print(cost_grasp_progress)
print(grasp_progress)

print(" ===========")
print(cost_sa_progress)
print(sa_progress)

fig = plt.figure(figsize=(14, 5))
ax1 = plt.subplot(1, 2, 1)
ax1.plot(cost_sa_progress,sa_progress,'g-',label = "Simulated Annealing")
ax1.plot(cost_grasp_progress,grasp_progress,'b-',label='GRASP')
ax1.legend(loc=0)
ax1.set_ylim(17,34)



ax2 = ax1.twiny()
ax2.plot(grasp_progress,'b-',label='GRASP')
#ax2.legend(['GRASP'])
ax2.legend(loc=0)



ax2 = plt.subplot(1, 2, 2)
ax2.plot(grasp_progress,'b-')
ax2.legend(['GRASP'])
ax2.set_ylim(17,34)

fig.text(0.3, 0.01, 'Computational cost', ha='center')
fig.text(0.07, 0.5, 'Objectives O1 + O4', va='center', rotation='vertical')
plt.savefig('iterations.pdf')
'''