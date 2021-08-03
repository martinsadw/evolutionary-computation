import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

import config
from fitness import Fitness
from algorithms.grasp import Grasp
from algorithms.brute_force import BruteForce
from algorithms.simulated_annealing import SimulatedAnnealing
from read.algorithm import create_results_name_list, get_results_name
from acs.objective import concepts_covered_function, materials_balancing_function
import pandas as pd
from acs.learning_material import LearningMaterial

def get_fitnessConcepts(new_concepts_materials):
    old_concept_coverage = config.instance.concepts_materials.copy()
    config.instance.concepts_materials = new_concepts_materials

    concepts_covered = 0
    materials_balancing = 0

    for student_id in range(config.num_students):
      concepts_covered += concepts_covered_function(config.recommendation[:, student_id], config.instance, student_id)
      materials_balancing += materials_balancing_function(config.recommendation[:, student_id], config.instance, student_id)
    
    config.instance.concepts_materials = old_concept_coverage
    concepts_covered = concepts_covered/config.num_students
    materials_balancing = materials_balancing/config.num_students
    
    return concepts_covered, materials_balancing


####### fitnessConcepts Before]

old_student_results = [Fitness.get_fitnessConcepts(student_id, config.concept_coverage.T) for student_id in range(config.num_students)]
student_results_before = sum(old_student_results)/config.num_students
print(f'student_results_before: {student_results_before}')
config.instance


# concepts_covered_before, materials_balancing_before = get_fitnessConcepts(config.concept_coverage.T)
# print("concepts_covered_before: ", concepts_covered_before)
# print("materials_balancing_before: ", materials_balancing_before)

# ####### fitnessConcepts After Grasp

'''
grasp = Grasp.from_config(os.path.join(config.dir, 'algorithms', 'config', 'config_grasp.ini'))
grasp_concept_coverage, student_results_grasp = grasp.run(config.concept_coverage, student_results_before)
print(f'student_results_grasp: {student_results_grasp}')


grasp_results = pickle.load( open( "results_grasp.pickle", "rb" ))
sa_results = pickle.load(open("results_SA.pickle","rb"))


grasp_concept_coverage = grasp_results["grasp_concept_coverage"]
grasp_fitness = grasp_results["grasp_fitness"]

cost_grasp = grasp_results['cost_progress']
print(cost_grasp)


cost_sa = sa_results['cost_progress']
'''

'''
grasp_student_results = [Fitness.get_fitnessConcepts(student_id, grasp_concept_coverage.T) for student_id in range(config.num_students)]

grasp_concepts_covered_after, grasp_materials_balancing_after = get_fitnessConcepts(grasp_concept_coverage.T)
'''


'''
count = 0
matrix_grasp = []
matrix_sa = []
#teste_cost_grasp = []

while(count<5):
  grasp = Grasp.from_config(os.path.join(config.dir, 'algorithms', 'config', 'config_grasp.ini'))
  grasp_concept_coverage, student_results_grasp = grasp.run(config.concept_coverage, student_results_before)
  grasp_results = pickle.load( open( "results_grasp.pickle", "rb" ))
  #grasp_progress = grasp_results["fitness_progress"]
  grasp_cost = grasp_results['cost_progress']

  simulatedAnnealing = SimulatedAnnealing.from_config(os.path.join(config.dir, 'algorithms', 'config', 'config_simulated_annealing.ini'))
  annealing_concept_coverage, student_results_annealing = simulatedAnnealing.run(config.concept_coverage, student_results_before)
  sa_results = pickle.load( open( "results_SA.pickle", "rb" ) )
  sa_cost = sa_results['cost_progress']
  #sa_progress = sa_results["fitness_progress"]

  matrix_grasp.append(grasp_cost)
  matrix_sa.append(sa_cost)
  count = count + 1
  print(count)

'''
'''
with open("matrix_grasp_sa_cost.pickle","wb") as file:
  pickle.dump({"cost_sa":cost_sa,"cost_grasp ":cost_grasp},file)
'''

  #cost_grasp_progress = grasp_results["cost_progress"]
  

####### fitnessConcepts Aftematrir Simulated Annealing
'''
simulatedAnnealing = SimulatedAnnealing.from_config(os.path.join(config.dir, 'algorithms', 'config', 'config_simulated_annealing.ini'))
annealing_concept_coverage, student_results_annealing = simulatedAnnealing.run(config.concept_coverage, student_results_before)
print(f'student_results_annealing: {student_results_annealing}')


sa_results = pickle.load( open( "results_SA.pickle", "rb" ) )
sa_concept_coverage = sa_results["sa_concept_coverage"]
annealing_student_results = [Fitness.get_fitnessConcepts(student_id, sa_concept_coverage.T) for student_id in range(config.num_students)]

sa_concepts_covered_after, sa_materials_balancing_after = get_fitnessConcepts(sa_concept_coverage.T)
print('----')
print("sa_concepts_covered_after: ", sa_concepts_covered_after)
print("sa_materials_balancing_after: ", sa_materials_balancing_after)
'''

########### Others fitness functions 


#bruteForce = BruteForce(sa_concept_coverage)
'''

bruteForce = BruteForce(grasp_concept_coverage)





old_difficulty = sum([Fitness.get_fitnessDifficulty(student_id, config.instance.materials_difficulty ,config.concept_coverage.T) for student_id in range(config.num_students)])/config.num_students
print(f'old_difficulty: {old_difficulty}')

new_difficulty = bruteForce.run("difficulty")


old_time = sum([Fitness.get_fitnessTime(student_id, config.instance.estimated_time.copy()) for student_id in range(config.num_students)])/config.num_students
print(f'old_student_results_time: {old_time}')

new_time =bruteForce.run("time")


m_active_reflexive = config.instance.materials_active_reflexive.copy()
m_sequential_global = config.instance.materials_sequential_global.copy()
m_sensory_intuitive = config.instance.materials_sensory_intuitive.copy()
m_visual_verbal = config.instance.materials_visual_verbal.copy()

m_learning_syle = {"active_reflexive": m_active_reflexive, "sequential_global": m_sequential_global, "visual_verbal": m_visual_verbal, "sensory_intuitive": m_sensory_intuitive}

old_LS = sum([Fitness.get_fitnessLearningStyle(student_id, m_learning_syle) for student_id in range(config.num_students)])/config.num_students
print(f'old_LS: {old_LS}')

new_learning_style = bruteForce.run("learning_syle")

with open('lom_data.pickle','wb') as file:
  pickle.dump({'time':new_time,'learning_style':new_learning_style,'difficulty':new_difficulty},file)

'''
#LearningMaterial(LearningMaterial.load_from_file('/mnt/c/Users/fonse/Documents/improving-LOR/instances/real/LOM/Algorithm/0.xml'))