import inspect
import numpy as np

import config
from fitness import Fitness

class BruteForce:
  def __init__(self, best_concept_coverage):
    self.best_concept_coverage = best_concept_coverage
    self.changed_materials = self.get_changed_materials(best_concept_coverage)
    self.materials_difficulty_values = np.array([1, 2, 3, 4, 5])
    self.material_duration_values = np.array([300, 600, 900, 1200, 1500, 1800]) # em minutos: 5, 10, 15, 20, 25, 30
    self.learning_style_dimentions = ["active_reflexive", "sensory_intuitive", "visual_verbal", "sequential_global"]
    self.learning_style_dimentions_values = np.array([-1, 1, 0])
    
  @staticmethod
  def get_changed_materials(best_concept_coverage):
    diff = best_concept_coverage != config.concept_coverage
    changed_mat = []
    for i, row in enumerate(diff):
      if(row.sum() > 0):
        changed_mat.append(i)
    return changed_mat
  
  def run(self, characteristic):
    if(characteristic == "difficulty"):
      old_materials_difficulty = config.instance.materials_difficulty.copy()
      new_materials_difficulty = self.__run(old_materials_difficulty, self.materials_difficulty_values, Fitness.get_fitnessDifficulty)
      
      new_difficulty = sum([Fitness.get_fitnessDifficulty(student_id, new_materials_difficulty, self.best_concept_coverage.T) for student_id in range(config.num_students)])/config.num_students
      print(new_materials_difficulty[self.changed_materials])
      print(f'new_difficulty: {new_difficulty}\n-----')
      
    elif(characteristic == "time"):
      old_material_duration = config.instance.estimated_time.copy()
      new_material_duration = self.__run(old_material_duration, self.material_duration_values, Fitness.get_fitnessTime)
      
      new_time = sum([Fitness.get_fitnessTime(student_id, new_material_duration) for student_id in range(config.num_students)])/config.num_students
      print(new_material_duration[self.changed_materials])
      print(f'new_time: {new_time}\n----')
      
    elif(characteristic == "learning_syle"):
      old_m_active_reflexive = config.instance.materials_active_reflexive.copy()
      old_m_sequential_global = config.instance.materials_sequential_global.copy()
      old_m_sensory_intuitive = config.instance.materials_sensory_intuitive.copy()
      old_m_visual_verbal = config.instance.materials_visual_verbal.copy()

      old_m_learning_syle = {"active_reflexive": old_m_active_reflexive, "sequential_global": old_m_sequential_global, "visual_verbal": old_m_visual_verbal, "sensory_intuitive": old_m_sensory_intuitive}
      
      new_m_learning_syle = old_m_learning_syle.copy()
      
      for dim in self.learning_style_dimentions:
        new_m_learning_syle[dim] = self.__run(old_m_learning_syle, self.learning_style_dimentions_values, Fitness.get_fitnessLearningStyle, dim)[dim]
      
      new_LS = sum([Fitness.get_fitnessLearningStyle(student_id, new_m_learning_syle) for student_id in range(config.num_students)])/config.num_students
      
      print(new_m_learning_syle["active_reflexive"][self.changed_materials])
      print(new_m_learning_syle["sequential_global"][self.changed_materials])
      print(new_m_learning_syle["visual_verbal"][self.changed_materials])
      print(new_m_learning_syle["sensory_intuitive"][self.changed_materials])
      print(f'new_LS: {new_LS}\n----')
              
    else:
      raise Exception('The {} value is not applicable.'.format(characteristic))
    
  def __run(self, characteristic_old_values, possible_values, fitness_function, dim = None):
    num_args = len(inspect.getfullargspec(fitness_function).args)
    characteristic_new_values = characteristic_old_values.copy()
    
    for mat in self.changed_materials:
      best_value = characteristic_old_values[mat] if dim is None else characteristic_old_values[dim][mat]
      if(num_args > 3):
        best_fitness = sum([fitness_function(student_id, characteristic_old_values, self.best_concept_coverage.T) for student_id in range(config.num_students)])/config.num_students
      else:
        best_fitness = sum([fitness_function(student_id, characteristic_old_values) for student_id in range(config.num_students)])/config.num_students
      
      for value in possible_values[possible_values != best_value]:
        if dim is None:
          characteristic_old_values[mat] = value
        else:
          characteristic_old_values[dim][mat] = value 
        if(num_args > 3):
          student_results_dif = sum([fitness_function(student_id, characteristic_old_values, self.best_concept_coverage.T) for student_id in range(config.num_students)])/config.num_students
        else:
          student_results_dif = sum([fitness_function(student_id, characteristic_old_values) for student_id in range(config.num_students)])/config.num_students
        
        if(student_results_dif < best_fitness):
          best_fitness = student_results_dif
          best_value = value
      
      if dim is None:
        characteristic_new_values[mat] = best_value
      else:
        characteristic_new_values[dim][mat] = best_value
    return characteristic_new_values