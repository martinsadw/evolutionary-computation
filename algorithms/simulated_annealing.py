import math
import pickle
import random
import logging
import argparse
from warnings import catch_warnings
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
    self.material = None
    self.deltaE = 0
    self.current_temperature = self.initial_temperature
    self.concepts_mask = np.zeros((num_materials,num_concepts))
    self.conflicts_order = {}
    self.concept_coverage = concept_coverage
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
    scaled_coverage = (concept_coverage * 2 - 1) # concept_coverage, onde False é -1 e True é 1   

    self.conflicts = student_difference * scaled_coverage
    
    change_potential = -np.minimum(0,self.conflicts).sum(axis=1) #somando as posições onde < 0 pois é onde há conflitos
    #change_potential = np.maximum(0, self.conflicts).sum(axis=1)
    self.orderOf_changed_materials = np.argsort(-change_potential).tolist()[:int(self.max_materials_changes)] #retorna os index que orderia o vetor change potential de forma descrescente
    
    #print('student yes: ', student_yes[40])
    #print('student no: ',student_no[40])
    #print('student diff: ',student_difference[40])
    #print('scaled coverage: ',scaled_coverage[40])
    #print('conflicts: ', self.conflicts[40])
    #print(np.argsort(self.conflicts[40]).tolist())
    #print('change potential:',change_potential[40])
    #print(self.orderOf_changed_materials)
    
    #print(self.orderOf_changed_materials)
    
  def get_randNeighbor(self, concept_coverage):
  
    concept_coverage_neighbor = concept_coverage.copy()

    if(len(self.materials_changed ) < self.max_materials_changes):
      selected_material_index = random.randrange(int(len(self.orderOf_changed_materials)))#indice do material dentro do orderOf
      self.material = self.orderOf_changed_materials[selected_material_index]
      self.materials_changed.append(self.material)
      del self.orderOf_changed_materials[selected_material_index]
      

    else:
      '''
      selected_undo_index = random.randrange(len(self.materials_changed))
      undo_material = self.materials_changed[selected_undo_index]
      self.orderOf_changed_materials.append(undo_material)
      del self.materials_changed[selected_undo_index]
      #print('material changed after:',len(self.materials_changed))
      concept_coverage_neighbor[undo_material] = concept_coverage[undo_material]
      '''
      selected_material_index = random.randrange(len(self.materials_changed))
      self.material = self.materials_changed[selected_material_index]
   
    if(self.material not in  self.conflicts_order.keys()):
      #filter = self.conflicts[self.material] < 0
      #concepts_conflicts = list(np.where(filter, self.conflicts[self.material], np.nan).argsort()[:filter.sum()])
      #self.conflicts_order[self.material] = concepts_conflicts
      self.conflicts_order[self.material] = np.argsort(self.conflicts[self.material]).tolist() 

    #conflicts_order = np.argsort(self.conflicts[self.material]).tolist() 
    num_iterations = random.randrange(self.max_concepts_changes)

    
    for k in range(num_iterations):
      #if(self.concepts_mask[self.material].sum() < self.max_concepts_changes):
            selected_concept_index = random.randrange(len(self.conflicts_order[self.material]))
            concept = self.conflicts_order[self.material][selected_concept_index]
            #del self.conflicts_order[self.material][selected_concept_index]          
            
            #if(self.conflicts[self.material,concept] > 0):
            self.concepts_mask[self.material,concept] = self.concepts_mask[self.material,concept] + 1
            concept_coverage_neighbor[self.material, concept] = ~concept_coverage_neighbor[self.material, concept] 

    
    count_changes = sum(i>0 for i in self.concepts_mask[self.material])
    #print(count_changes)
    if(count_changes > self.max_concepts_changes):
      changed_concepts = [idx for idx, val in enumerate(self.concepts_mask[self.material]) if val > 0] #pegando o indices dos conceitos que foram alterados
      
      #print('changed concepts before',len(changed_concepts))
      for i in  range(len(self.concept_coverage[self.material])):
        if(self.concept_coverage[self.material,i] == concept_coverage_neighbor[self.material,i]):
           if i in changed_concepts:
             del changed_concepts[changed_concepts.index(i)] #tirando dos changed concepts  os conceitos que foram alterados porem estão igual antes por multiplas alterações

      #print('changed concepts after' ,len(changed_concepts))

      while(self.max_concepts_changes < len(changed_concepts) ): #revertendo conceitos que foram modificados e estão diferentes até o limite
        selected_undo_concept_index = random.randrange(len(changed_concepts))
        concept_coverage_neighbor[self.material,changed_concepts[selected_undo_concept_index]] = ~concept_coverage_neighbor[self.material,changed_concepts[selected_undo_concept_index]]
        del changed_concepts[selected_undo_concept_index]

      #print('final changed concepts: ',len(changed_concepts))
    
     
    #print(self.concept_coverage[self.material])  

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
    
    self.current_temperature = self.initial_temperature
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
        
        self.deltaE = next_fitness - current_fitness
        
        #print('deltaE:', deltaE)
        if(self.deltaE < 0.0):
          current_solution = next_solution
          current_fitness = next_fitness
          
          if(next_fitness < best_fitness  ):
            best_solution = next_solution
            best_fitness = next_fitness
        else:
          if(random.uniform(0,1) < math.exp(-self.deltaE / self.current_temperature)):
            current_solution = next_solution
            current_fitness = next_fitness
            
            #print('current fitness: ', current_fitness)
      
      self.current_temperature = self.decreaseTemperature(self.current_temperature)
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