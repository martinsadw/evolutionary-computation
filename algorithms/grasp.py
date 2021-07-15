import random
import pickle
import logging
import argparse
from typing import Counter
import numpy as np
import configparser

from fitness import Fitness
from config import instance, concept_coverage, objectives, num_students, num_concepts, num_materials, recommendation, dir

class Grasp:
  def __init__(self, max_counter_fitness, local_search_size, max_materials_changes, max_concepts_changes, seed):
    
    self.max_counter_fitness = max_counter_fitness
    self.local_search_size = local_search_size
    self.max_materials_changes = max_materials_changes
    self.max_concepts_changes = max_concepts_changes
    self.seed = seed
    self.concepts_mask = np.zeros((num_materials,num_concepts))  
    self.concept_coverage = concept_coverage
    self.change_potential_order = []
    self.material = None
    self.materials_changed = []
    self.fitness_progress = []

    self.conflicts_order = {}
    self.cost_counter = 0
    self.count = 0
  @classmethod
  def from_config(cls, config_filename):
    config = configparser.ConfigParser(inline_comment_prefixes=("#",))
    config.read(config_filename)
    
    max_counter_fitness = int(config['default']['max_counter_fitness'])
    local_search_size = int(config['default']['local_search_size'])
    #alpha_m = float(config['default']['alpha_m'])
    #alpha_c = float(config['default']['alpha_c'])
    max_materials_changes = float(config['default']['max_materials_changes'])
    max_concepts_changes = float(config['default']['max_concepts_changes'])
    seed = int(config['default']['seed'])
    
    #return cls(max_iterations, local_search_size, alpha_m, alpha_c, max_materials_changes, max_concepts_changes, seed)  
    return cls(max_counter_fitness, local_search_size, max_materials_changes, max_concepts_changes, seed)
  
  
  def counter_fitness(self,solution):
    self.cost_counter +=1
    return sum([Fitness.get_fitnessConcepts(student_id, solution.T) for student_id in range(num_students)])/num_students        
 
  def run(self, concept_coverage, fitnessConcepts_total, DATFILE=None):
    
    best_solution = concept_coverage
    best_fitness = fitnessConcepts_total
    cost_progress = []
    while(self.cost_counter<self.max_counter_fitness):
      solution, solution_fitness, materials_changed = self.greadyRandomizedConstruction()
      solution, solution_fitness = self.localSearch(solution, solution_fitness, materials_changed)
      
      if(solution_fitness < best_fitness):
        best_solution = solution
        best_fitness = solution_fitness
    
      self.fitness_progress.append(best_fitness)
      cost_progress.append(self.cost_counter)
    
    if(DATFILE):
      with open(DATFILE, 'w') as f:
        f.write(str(best_fitness))
    else:
      with open('results_grasp.pickle', 'wb') as file:
        pickle.dump({"fitness_progress": self.fitness_progress, "grasp_concept_coverage": best_solution, "grasp_fitness": best_fitness,"cost_progress":cost_progress}, file)
      
      return best_solution, best_fitness
  
  
  def greadyRandomizedConstruction(self):
    student_yes = np.matmul(recommendation.astype(int), objectives.astype(int)) #quantos alunos receberam o material E o tem como objetivo
    student_no = np.matmul(recommendation.astype(int), (~objectives).astype(int)) #quantos alunos receberam o material E não o tem como objetivo
    student_difference = student_no - student_yes #(quantos alunos querem ter o conveito adicionado) - (quantos alunos querem ter o conceito removido)
    scaled_coverage = (concept_coverage * 2 - 1) # concept_coverage, onde False é -1 e True é 1
    conflicts = student_difference * scaled_coverage
    change_potential = -np.minimum(0,conflicts).sum(axis=1) #somando as posições onde < 0 pois é onde há conflitos
    new_concept_coverage = concept_coverage.copy()
    self.change_potential_order = np.argsort(-change_potential).tolist()[:int(self.max_materials_changes)]
    
    for j in range(int(self.max_materials_changes)):
      # Select a material and remove from the list
      selected_material_index = random.randrange(int(len(self.change_potential_order)))
      
      self.material = self.change_potential_order[selected_material_index]
      self.materials_changed.append(self.material)
      del self.change_potential_order[selected_material_index]
  

      if(self.material not in  self.conflicts_order.keys()):
          self.conflicts_order[self.material] = np.argsort(-conflicts[self.material]).tolist()
  
      for k in range(int(self.max_concepts_changes)):
        # Select a concept from the material and remove from the list
        selected_concept_index = random.randrange(len(self.conflicts_order[self.material]))
        concept = self.conflicts_order[self.material][selected_concept_index]
        self.concepts_mask[self.material,concept] = self.concepts_mask[self.material,concept] + 1
        new_concept_coverage[self.material, concept] = ~new_concept_coverage[self.material, concept]

      count_changes = sum(i>0 for i in self.concepts_mask[self.material])
      if(count_changes > self.max_concepts_changes):
          changed_concepts = [idx for idx, val in enumerate(self.concepts_mask[self.material]) if val > 0] #pegando o indices dos conceitos que foram alterados
      
          for i in  range(len(self.concept_coverage[self.material])):
            if(self.concept_coverage[self.material,i] == new_concept_coverage[self.material,i]):
                if i in changed_concepts:
                  del changed_concepts[changed_concepts.index(i)] #tirando dos changed concepts  os conceitos que foram alterados porem estão igual antes por multiplas alterações
      
          while(self.max_concepts_changes < len(changed_concepts) ): #revertendo conceitos que foram modificados e estão diferentes até o limitante
            selected_undo_concept_index = random.randrange(len(changed_concepts))
            new_concept_coverage[self.material,changed_concepts[selected_undo_concept_index]] = ~new_concept_coverage[self.material,changed_concepts[selected_undo_concept_index]]
            del changed_concepts[selected_undo_concept_index]
    
    new_best_fitness = self.counter_fitness(new_concept_coverage)
    return new_concept_coverage, new_best_fitness, self.materials_changed
  

  def localSearch(self, solution, solution_fitness, materials_changed):
  

    new_concept_coverage = solution
    new_best_fitness = solution_fitness
    materials_changed_mask = np.zeros((num_materials,num_concepts)) #salvando as posições dos conceitos que foram alterados dos materiais
  
    teste = 0
    for j in range(len(materials_changed)):
      for i in  range(num_concepts):
          if(self.concept_coverage[materials_changed[j],i] != solution[materials_changed[j],i]): #materials change just has less than the maximum  concept change and differnete from the inital solution 
              materials_changed_mask[materials_changed[j],i] = 1 #colocando 1 nas posições que já foram alteradas
    
    #materials come with the max or less than the max concepts changes

    for j in range(self.local_search_size):  
        fitness_improved = False        
        if(self.cost_counter>=self.max_counter_fitness):
              break
        for material in materials_changed:
            if(self.cost_counter>=self.max_counter_fitness):
              break
            for concept in range(num_concepts):
              if(self.cost_counter>=self.max_counter_fitness):
                break

              step_concept_coverage = new_concept_coverage.copy()
              step_concept_coverage[material, concept] = ~step_concept_coverage[material, concept]
              materials_changed_mask[material,concept] = materials_changed_mask[material,concept] +1             
              changed_concepts = [idx for idx, val in enumerate(materials_changed_mask[material]) if val > 0] #pegando o indices dos conceitos que foram alterados
              
              for i in  range(num_concepts):
                  if(self.concept_coverage[material,i] == step_concept_coverage[material,i]):
                      if i in changed_concepts:
                        del changed_concepts[changed_concepts.index(i)] 

              while(self.max_concepts_changes < len(changed_concepts)): #testar, se ainda nao funcionar, comparar os conceitos que foram alterados com os conceitos antigos   
                selected_undo_concept_index = random.randrange(len(changed_concepts))
                step_concept_coverage[material,changed_concepts[selected_undo_concept_index]] = ~step_concept_coverage[material,changed_concepts[selected_undo_concept_index]]
                del changed_concepts[selected_undo_concept_index]
              
              step_fitness = self.counter_fitness(step_concept_coverage)
              
              if new_best_fitness > step_fitness:
                  new_best_fitness = step_fitness
                  new_concept_coverage = step_concept_coverage
                  fitness_improved = True
                  
                  
                  
        if fitness_improved:
            break
    
    return new_concept_coverage, new_best_fitness
  

  def __repr__(self):
    return f'\n max_iterations: {self.max_iterations}\n local_search_size: {self.local_search_size}\n alpha_m: {self.alpha_m}\n alpha_c: {self.alpha_c}\n max_materials_changes: {self.max_materials_changes}\n max_concepts_changes: {self.max_concepts_changes}\n seed: {self.seed}\n'
  
if __name__ == '__main__':
  ap = argparse.ArgumentParser(description='Feature Selection using GA with DecisionTreeClassifier')
  ap.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
  ap.add_argument('--max_counter_fitness', type=int, default=3000, help='Cost limitation')
  ap.add_argument('--local_search_size', type=int, default=2, help='Number of iterations in local search')
  ap.add_argument('-mc','--max_materials_changes',default=10,help="max materials")
  ap.add_argument('-cc','--max_concepts_changes',default=5,help="max concepts")
  #ap.add_argument('--alpha_m', type=float, default=0.2, help='alpha of materials')
  #ap.add_argument('--alpha_c', type=float, default=0.3, help='alpha of concepts')
  ap.add_argument('--datfile', dest='datfile', type=str, help='File where it will be save the score (result)')

  args = ap.parse_args()

  if args.verbose:
      logging.basicConfig(level=logging.DEBUG)

  logging.debug(args)
  
  student_results_before = sum([Fitness.get_fitnessConcepts(student_id, concept_coverage.T) for student_id in range(num_students)])/num_students
  
  grasp = Grasp(args.max_counter_fitness, args.local_search_size, args.max_materials_changes,args.max_concepts_changes, 98092891)
  
  grasp.run(concept_coverage, student_results_before, args.datfile)
  # grasp_concept_coverage, student_results_grasp = grasp.run(concept_coverage, student_results_before)
  # print(f'student_results_grasp: {student_results_grasp}')