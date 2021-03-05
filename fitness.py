import config
import numpy as np
from acs.objective import concepts_covered_function, materials_balancing_function, learning_style_function, difficulty_function, total_time_function

class Fitness:
  instance = config.instance
  recommendation = config.recommendation
  
  @classmethod
  def get_fitnessConcepts(cls, student_id, new_concepts_materials):
    old_concept_coverage = cls.instance.concepts_materials.copy()
    cls.instance.concepts_materials = new_concepts_materials

    concepts_covered = concepts_covered_function(cls.recommendation[:, student_id], cls.instance, student_id)
    materials_balancing = materials_balancing_function(cls.recommendation[:, student_id], cls.instance, student_id)
    
    fitnessConcepts = concepts_covered + materials_balancing

    cls.instance.concepts_materials = old_concept_coverage
    
    return fitnessConcepts
  
  @classmethod
  def get_fitnessDifficulty(cls, student_id, materials_difficulty, covered_concepts):
    old_material_difficulty = cls.instance.materials_difficulty.copy()
    cls.instance.materials_difficulty = materials_difficulty
    
    old_concept_coverage = cls.instance.concepts_materials.copy()
    cls.instance.concepts_materials = covered_concepts
    
    fitness = difficulty_function(cls.recommendation[:, student_id], cls.instance, student_id)
    
    cls.instance.concepts_materials = old_concept_coverage
    cls.instance.materials_difficulty = old_material_difficulty
    return fitness
  
  @classmethod
  def get_fitnessTime(cls, student_id, estimate_time):
    old_estimate_time = cls.instance.estimated_time
    cls.instance.estimated_time = estimate_time
    
    fitness = total_time_function(cls.recommendation[:, student_id], cls.instance, student_id)
    
    cls.instance.estimated_time = old_estimate_time
    return fitness
  
  @classmethod
  def get_fitnessLearningStyle(cls, student_id, m_learning_style = None):
    materials_active_reflexive = cls.instance.materials_active_reflexive.copy()
    materials_sensory_intuitive = cls.instance.materials_sensory_intuitive.copy()
    materials_visual_verbal = cls.instance.materials_visual_verbal.copy()
    materials_sequential_global = cls.instance.materials_sequential_global.copy()
    
    if m_learning_style:
      cls.instance.materials_active_reflexive = m_learning_style['active_reflexive']
      cls.instance.materials_sensory_intuitive = m_learning_style['sensory_intuitive']
      cls.instance.materials_visual_verbal = m_learning_style['visual_verbal']
      cls.instance.materials_sequential_global = m_learning_style['sequential_global']
    
    fitness = learning_style_function(cls.recommendation[:, student_id], cls.instance, student_id)
    
    cls.instance.materials_active_reflexive = materials_active_reflexive 
    cls.instance.materials_sensory_intuitive = materials_sensory_intuitive
    cls.instance.materials_visual_verbal = materials_visual_verbal    
    cls.instance.materials_sequential_global = materials_sequential_global
    
    return fitness