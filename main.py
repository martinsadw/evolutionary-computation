import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

import config
from fitness import Fitness
from algorithms.grasp import Grasp
from algorithms.simulated_annealing import SimulatedAnnealing
from read.algorithm import create_results_name_list, get_results_name
from acs.objective import concepts_covered_function, materials_balancing_function

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


####### fitnessConcepts Before
# old_student_results = [Fitness.get_fitnessConcepts(student_id, config.concept_coverage.T) for student_id in range(config.num_students)]
# student_results_before = sum(old_student_results)/config.num_students
# print(f'student_results_before: {student_results_before}')


# concepts_covered_before, materials_balancing_before = get_fitnessConcepts(config.concept_coverage.T)
# print("concepts_covered_before: ", concepts_covered_before)
# print("materials_balancing_before: ", materials_balancing_before)

# ####### fitnessConcepts After Grasp
# grasp = Grasp.from_config(os.path.join(config.dir, 'algorithms', 'config', 'config_grasp.ini'))
# grasp_concept_coverage, student_results_grasp = grasp.run(config.concept_coverage, student_results_before)
# print(f'student_results_grasp: {student_results_grasp}')

grasp_results = pickle.load( open( "results_grasp_best.pickle", "rb" ) )
grasp_concept_coverage = grasp_results["grasp_concept_coverage"]
grasp_fitness = grasp_results["grasp_fitness"]

# grasp_student_results = [Fitness.get_fitnessConcepts(student_id, grasp_concept_coverage.T) for student_id in range(config.num_students)]

# grasp_concepts_covered_after, grasp_materials_balancing_after = get_fitnessConcepts(grasp_concept_coverage.T)
# print("-----")
# print("grasp_concepts_covered_after: ", grasp_concepts_covered_after)
# print("grasp_materials_balancing_after: ", grasp_materials_balancing_after)

# ####### fitnessConcepts After Simulated Annealing

simulatedAnnealing = SimulatedAnnealing.from_config(os.path.join(config.dir, 'algorithms', 'config', 'config_simulated_annealing.ini'))
annealing_concept_coverage, student_results_annealing = simulatedAnnealing.run(grasp_concept_coverage, grasp_fitness)
print(f'student_results_annealing: {student_results_annealing}')

# sa_results = pickle.load( open( "results_SA.pickle", "rb" ) )
# sa_concept_coverage = sa_results["sa_concept_coverage"]

# annealing_student_results = [Fitness.get_fitnessConcepts(student_id, sa_concept_coverage.T) for student_id in range(config.num_students)]

# sa_concepts_covered_after, sa_materials_balancing_after = get_fitnessConcepts(sa_concept_coverage.T)
# print('----')
# print("sa_concepts_covered_after: ", sa_concepts_covered_after)
# print("sa_materials_balancing_after: ", sa_materials_balancing_after)



########### Others fitness functions 

# old_difficulty = sum([Fitness.get_fitnessDifficulty(student_id, config.instance.materials_difficulty ,config.concept_coverage.T) for student_id in range(config.num_students)])/config.num_students
# print(f'old_difficulty: {old_difficulty}')

# diff = grasp_concept_coverage != config.concept_coverage
# changed_mat = []
# for i, row in enumerate(diff):
#   if(row.sum() > 0):
#     changed_mat.append(i)

# for mat in changed_mat:
#   print(mat)
#   for i, c in enumerate(grasp_concept_coverage[mat]):
#     print(config.instance.concepts_keys[i])
#   print("---")
  
# materials_difficulty = config.instance.materials_difficulty.copy()
# new_materials_difficulty = config.instance.materials_difficulty.copy()
# possible_values = np.array([1, 2, 3, 4, 5])
# for mat in changed_mat:
#   best_value = materials_difficulty[mat]
#   best_fitness = sum([Fitness.get_fitnessDifficulty(student_id, materials_difficulty, grasp_concept_coverage.T) for student_id in range(config.num_students)])/config.num_students
  
#   for value in possible_values[possible_values != best_value]:
#     materials_difficulty[mat] = value
#     student_results_dif = sum([Fitness.get_fitnessDifficulty(student_id, materials_difficulty, grasp_concept_coverage.T) for student_id in range(config.num_students)])/config.num_students
#     if(student_results_dif < best_fitness):
#       best_fitness = student_results_dif
#       best_value = value
  
#   new_materials_difficulty[mat] = best_value
   
# new_difficulty = sum([Fitness.get_fitnessDifficulty(student_id, new_materials_difficulty ,grasp_concept_coverage.T) for student_id in range(config.num_students)])/config.num_students
# print(f'new_difficulty: {new_difficulty}\n-----')

# print("dificuldade:")
# print(new_materials_difficulty[changed_mat])
# print("")

# ### tempo 

# old_time = sum([Fitness.get_fitnessTime(student_id, config.instance.estimated_time.copy()) for student_id in range(config.num_students)])/config.num_students
# print(f'old_student_results_time: {old_time}')

# material_duration = config.instance.estimated_time.copy()
# new_material_duration = config.instance.estimated_time.copy()

# possible_duration = [300, 600, 900, 1200, 1500, 1800] # em minutos: 5, 10, 15, 20, 25, 30
# for mat in changed_mat:
#   best_value = material_duration[mat]
#   best_fitness = sum([Fitness.get_fitnessTime(student_id, material_duration) for student_id in range(config.num_students)])/config.num_students
  
#   for value in possible_duration:
#     material_duration[mat] = value
#     student_results_dif = sum([Fitness.get_fitnessTime(student_id, material_duration) for student_id in range(config.num_students)])/config.num_students
#     if(student_results_dif < best_fitness):
#       best_fitness = student_results_dif
#       best_value = value
  
#   new_material_duration[mat] = best_value

# new_time = sum([Fitness.get_fitnessTime(student_id, new_material_duration) for student_id in range(config.num_students)])/config.num_students
# print(f'new_time: {new_time}\n----')

# print("tempo:")
# print(new_material_duration[changed_mat])
# print("")
# # learning style


# new_m_active_reflexive = config.instance.materials_active_reflexive.copy()
# new_m_sequential_global = config.instance.materials_sequential_global.copy()
# new_m_sensory_intuitive = config.instance.materials_sensory_intuitive.copy()
# new_m_visual_verbal = config.instance.materials_visual_verbal.copy()

# new_m_learning_syle = {"active_reflexive": new_m_active_reflexive, "sequential_global": new_m_sequential_global, "visual_verbal": new_m_visual_verbal, "sensory_intuitive": new_m_sensory_intuitive} 

# m_active_reflexive = config.instance.materials_active_reflexive.copy()
# m_sequential_global = config.instance.materials_sequential_global.copy()
# m_sensory_intuitive = config.instance.materials_sensory_intuitive.copy()
# m_visual_verbal = config.instance.materials_visual_verbal.copy()


# m_learning_syle = {"active_reflexive": m_active_reflexive, "sequential_global": m_sequential_global, "visual_verbal": m_visual_verbal, "sensory_intuitive": m_sensory_intuitive}

# old_LS = sum([Fitness.get_fitnessLearningStyle(student_id, m_learning_syle) for student_id in range(config.num_students)])/config.num_students
# print(f'old_LS: {old_LS}')


# for mat in changed_mat:
#   ls_dimention_count = {
#     "active_reflexive": [-1, 1, 0],
#     "sensory_intuitive": [-1, 1, 0],
#     "visual_verbal": [-1, 1, 0],
#     "sequential_global": [-1, 1, 0]
#   }
  
#   for dim in ls_dimention_count.keys():
#     best_value = m_learning_syle[dim][mat]
#     best_fitness = sum([Fitness.get_fitnessLearningStyle(student_id, m_learning_syle) for student_id in range(config.num_students)])/config.num_students
#     for value in ls_dimention_count[dim]:
#       if value == best_value:
#         break
#       m_learning_syle[dim][mat] = value
#       student_results_dif = sum([Fitness.get_fitnessLearningStyle(student_id, m_learning_syle) for student_id in range(config.num_students)])/config.num_students
#       if(student_results_dif < best_fitness):
#         best_fitness = student_results_dif
#         best_value = value
        
#     new_m_learning_syle[dim][mat] = best_value
    
     
# new_LS = sum([Fitness.get_fitnessLearningStyle(student_id, new_m_learning_syle) for student_id in range(config.num_students)])/config.num_students
# print(f'new_LS: {new_LS}')

# print("LS:")
# print(new_m_learning_syle["active_reflexive"][changed_mat])
# print(new_m_learning_syle["sequential_global"][changed_mat])
# print(new_m_learning_syle["visual_verbal"][changed_mat])
# print(new_m_learning_syle["sensory_intuitive"][changed_mat])
# print("")