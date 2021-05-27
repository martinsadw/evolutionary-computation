import math
import pickle
import random
import logging
import argparse
import numpy as np
import configparser

from fitness import Fitness
from config import instance, concept_coverage, objectives, num_students, num_concepts, num_materials, recommendation

class SimulatedAnnealing:
  def __init__(self, max_iterations, cycle, initial_temperature, final_temperature, alpha, beta, max_materials_changes, max_concepts_changes, seed):
    self.max_iterations = max_iterations
    self.cycle = cycle
    self.initial_temperature = initial_temperature
    self.final_temperature = final_temperature
    self.alpha = alpha
    self.beta = beta
    self.max_materials_changes = max_materials_changes
    self.max_concepts_changes = max_concepts_changes
    self.seed = seed
    self.materials_changed = []
    self.orderOf_changed_materials = []
    self.conflicts = []
   
   
  @classmethod
  def from_config(cls, config_filename):
    config = configparser.ConfigParser(inline_comment_prefixes=("#",))
    config.read(config_filename)
    
    max_iterations = int(config['default']['max_iterations'])
    cycle = int(config['default']['cycle'])
    initial_temperature = float(config['default']['initial_temperature'])
    final_temperature = float(config['default']['final_temperature'])
    alpha = float(config['default']['alpha'])
    beta = float(config['default']['beta'])
    max_materials_changes = float(config['default']['max_materials_changes'])
    max_concepts_changes = float(config['default']['max_concepts_changes'])
    seed = int(config['default']['seed'])
    
    return cls(max_iterations, cycle, initial_temperature, final_temperature, alpha, beta, max_materials_changes, max_concepts_changes, seed)
    
  def get_orderOfModifiedMaterials(self):
    
    student_yes = np.matmul(recommendation.astype(int), objectives.astype(int)) #quantos alunos receberam o material E o tem como objetivo
    student_no = np.matmul(recommendation.astype(int), (~objectives).astype(int)) #quantos alunos receberam o material E não o tem como objetivo
    student_difference = student_no - student_yes #(quantos alunos querem ter o conceito adicionado) - (quantos alunos querem ter o conceito removido)
    #student_difference = student_yes
    scaled_coverage = (concept_coverage * 2 - 1) # concept_coverage, onde False é -1 e True é 1   

    self.conflicts = student_difference * scaled_coverage
    change_potential = np.maximum(0, self.conflicts).sum(axis=1) #np.maximum(0, self.conflicts) >>> replace nos numeros negativos com 0
    
    '''
    print('student difference',student_difference[1])
    print('scaled coverage',scaled_coverage[1])
    print('concept coverage',concept_coverage[1])
    print('conflicts',self.conflicts[1])
    print('change potential',change_potential[1])
    print(np.maximum(0, self.conflicts)[1])
    '''
    self.orderOf_changed_materials = np.argsort(-change_potential).tolist() #retorna os index que orderia o vetor change potential de forma cresce
    #print('orderOf_changed_materials: ', self.orderOf_changed_materials)

  def get_randNeighbor(self, concept_coverage):
  
    concept_coverage_neighbor = concept_coverage.copy()
    selected_material_index = random.randrange(int(len(self.orderOf_changed_materials)*0.95))
    
    material = random.choice(self.orderOf_changed_materials)
    #material = self.orderOf_changed_materials[0]
    #material = self.orderOf_changed_materials[selected_material_index]

    if(len(self.materials_changed) > self.max_materials_changes ): #<<<

            selected_undo_index = random.randrange(len(self.materials_changed))
            undo_material = self.materials_changed[selected_undo_index]
            self.orderOf_changed_materials.append(undo_material)
            del self.materials_changed[selected_undo_index]
            #print('material changed after:',len(self.materials_changed))
            concept_coverage_neighbor[undo_material] = concept_coverage[undo_material]
            
            #print(self.materials_changed)

    self.materials_changed.append(selected_material_index)
    del self.orderOf_changed_materials[selected_material_index]

    conflicts_order = np.argsort(-self.conflicts[material]).tolist()
    num_iterations = random.randrange(self.max_concepts_changes ) 
    #num_iterations = int(self.max_concepts_changes * num_concepts*current_temperature_factor)
 
    for k in range(num_iterations):
        selected_concept_index = random.randrange(len(conflicts_order))
        concept = conflicts_order[selected_concept_index]
        del conflicts_order[selected_concept_index]

        if self.conflicts[material, concept] > 0:
          concept_coverage_neighbor[material, concept] = ~concept_coverage_neighbor[material, concept]
    
    return concept_coverage_neighbor
  
  
  def decreaseTemperature(self, temperature, cycle=None, method='geometric'):
    if(method == "geometric"):
      return temperature * self.alpha
    if(method == "beta"):
      return temperature / (1 + self.beta * temperature)
    if(method  == "logarithmical-multiplicative-cooling"):
      return temperature / (1 + 1.3*math.log(1 + cycle))
    if(method == "linear-multiplicative-cooling"):
      return temperature / (1 + 1.3 * cycle)
      
  
  def run(self, concept_coverage, fitnessConcepts_total, DATFILE=None):
    
    best_solution = concept_coverage
    best_fitness = fitnessConcepts_total
    
    current_temperature = self.initial_temperature
    current_solution = concept_coverage

    current_fitness = fitnessConcepts_total
    
    self.get_orderOfModifiedMaterials()
    fitness_progress = np.empty(self.max_iterations)
    
    for i in range(self.max_iterations):
      for l in range(self.cycle):
         
        #current_temperature_factor = current_temperature/self.initial_temperature
        #next_solution = self.get_randNeighbor(best_solution,current_temperature_factor)
        
        next_solution = self.get_randNeighbor(best_solution)
        next_fitness = sum([Fitness.get_fitnessConcepts(student_id, next_solution.T) for student_id in range(num_students)])/num_students        
        
        deltaE = next_fitness - current_fitness
        
        #print('deltaE:', deltaE)
        if(deltaE < 0.0):
          current_solution = next_solution
          current_fitness = next_fitness
          
          if(next_fitness < best_fitness  ):
            best_solution = next_solution
            best_fitness = next_fitness
        else:
          if(random.uniform(0,1) < math.exp(-deltaE / current_temperature)):
            current_solution = next_solution
            current_fitness = next_fitness
            
            #print('current fitness: ', current_fitness)
      
      current_temperature = self.decreaseTemperature(current_temperature)
      fitness_progress[i] = best_fitness
      
    # print("current_temperature: ", current_temperature)
    if(DATFILE):
      with open(DATFILE, 'w') as f:
        f.write(str(best_fitness))
    else:
      with open('results_SA.pickle', 'wb') as file:
        pickle.dump({"fitness_progress": fitness_progress, "sa_concept_coverage": best_solution, "sa_fitness": best_fitness}, file)
        
      return best_solution, best_fitness

  def __repr__(self):
    return f'\n max_iterations: {self.max_iterations}\n cycle: {self.cycle}\n initial_temperature: {self.initial_temperature}\n final_temperature: {self.final_temperature}\n alpha: {self.alpha}\n max_materials_changes: {self.max_materials_changes}\n max_concepts_changes: {self.max_concepts_changes}\n seed: {self.seed}\n'

if __name__ == '__main__':
  ap = argparse.ArgumentParser(description='Simulated Annealing parameters definition')
  ap.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
  ap.add_argument('-i', '--max_iterations', type=int, default=100, help='Number of iterations')
  ap.add_argument('-c', '--cycle', type=int, default=2, help='Number of cycles per temperature')
  ap.add_argument('-it', '--initial_temperature', default=1000.0, type=float,  help='Initial temperature')
  ap.add_argument('-ft', '--final_temperature', default=0.001, type=float,  help='Final temperature')
  ap.add_argument('-a', '--alpha', type=float, default=0.90,  help='alpha')
  ap.add_argument('-b', '--beta', type=str,  default=0.2, help='beta')
  ap.add_argument('--datfile', dest='datfile', type=str, help='File where it will be save the score (result)')

  args = ap.parse_args()

  if args.verbose:
      logging.basicConfig(level=logging.DEBUG)

  logging.debug(args)
  
  student_results_before = sum([Fitness.get_fitnessConcepts(student_id, concept_coverage.T) for student_id in range(num_students)])/num_students
  
  
  simulatedAnnealing = SimulatedAnnealing(args.max_iterations, args.cycle, args.initial_temperature, args.final_temperature, args.alpha, args.beta, 0.0356, 0.1667, 98092891)
  
  simulatedAnnealing.run(concept_coverage, student_results_before, args.datfile)
  # annealing_concept_coverage, student_results_annealing = simulatedAnnealing.run(concept_coverage, student_results_before)
  # print(f'student_results_annealing: {student_results_annealing}')