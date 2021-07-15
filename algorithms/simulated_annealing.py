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
  def __init__(self,max_counter_fitness,cycle, initial_temperature, alpha, beta, max_materials_changes, max_concepts_changes, seed):
    #self.max_iterations = max_iterations
    self.max_counter_fitness =max_counter_fitness
    self.cycle = cycle
    self.initial_temperature = initial_temperature
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
    self.cost_counter= 0
    self.concepts_mask = np.zeros((num_materials,num_concepts))
    self.conflicts_order = {}
    self.concept_coverage = concept_coverage

  @classmethod
  def from_config(cls, config_filename):
    config = configparser.ConfigParser(inline_comment_prefixes=("#",))
    config.read(config_filename)
    
    max_counter_fitness = int(config['default']['max_counter_fitness'])
    cycle = int(config['default']['cycle'])
    initial_temperature = float(config['default']['initial_temperature'])
    alpha = float(config['default']['alpha'])
    beta = float(config['default']['beta'])
    max_materials_changes = float(config['default']['max_materials_changes'])
    max_concepts_changes = float(config['default']['max_concepts_changes'])
    seed = int(config['default']['seed'])
    
    return cls(max_counter_fitness, cycle, initial_temperature, alpha, beta, max_materials_changes, max_concepts_changes, seed)
  
  def counter_fitness(self,solution):
    self.cost_counter+=1
    return sum([Fitness.get_fitnessConcepts(student_id, solution.T) for student_id in range(num_students)])/num_students        
 



  def get_orderOfModifiedMaterials(self):
    
    student_yes = np.matmul(recommendation.astype(int), objectives.astype(int)) #quantos alunos receberam o material E o tem como objetivo
    student_no = np.matmul(recommendation.astype(int), (~objectives).astype(int)) #quantos alunos receberam o material E não o tem como objetivo
    student_difference = student_no - student_yes #(quantos alunos querem ter o conceito adicionado) - (quantos alunos querem ter o conceito removido)
    scaled_coverage = (concept_coverage * 2 - 1) # concept_coverage, onde False é -1 e True é 1   
    self.conflicts = student_difference * scaled_coverage
    change_potential = -np.minimum(0,self.conflicts).sum(axis=1) #somando as posições onde < 0 pois é onde há conflitos
    #change_potential = np.maximum(0, self.conflicts).sum(axis=1)
    self.orderOf_changed_materials = np.argsort(-change_potential).tolist()[:int(self.max_materials_changes)] #retorna os index que orderia o vetor change potential de forma descrescente
   

  def get_randNeighbor(self, concept_coverage):
  
    concept_coverage_neighbor = concept_coverage.copy()

    if(len(self.materials_changed ) < self.max_materials_changes):
      selected_material_index = random.randrange(int(len(self.orderOf_changed_materials)))#indice do material dentro do orderOf
      self.material = self.orderOf_changed_materials[selected_material_index]
      self.materials_changed.append(self.material)
      del self.orderOf_changed_materials[selected_material_index]
      
    else:
      selected_material_index = random.randrange(len(self.materials_changed))
      self.material = self.materials_changed[selected_material_index]
   
    if(self.material not in  self.conflicts_order.keys()): #verificando se o material já está dentro do conflicts order
      self.conflicts_order[self.material] = np.argsort(self.conflicts[self.material]).tolist() 
    
    num_iterations = random.randrange(self.max_concepts_changes)

    
    for k in range(num_iterations):
            selected_concept_index = random.randrange(len(self.conflicts_order[self.material]))
            concept = self.conflicts_order[self.material][selected_concept_index]
            self.concepts_mask[self.material,concept] = self.concepts_mask[self.material,concept] + 1
            concept_coverage_neighbor[self.material, concept] = ~concept_coverage_neighbor[self.material, concept] 

    
    count_changes = sum(i>0 for i in self.concepts_mask[self.material]) #somando para o material, o número de conceitos que foram modificados
   
    if(count_changes > self.max_concepts_changes): #se o numero de alterações dos conceitos do material for maior que o máximo, salvar o index dos conceitos que foram modificados
      changed_concepts = [idx for idx, val in enumerate(self.concepts_mask[self.material]) if val > 0] #salvando os indices dos conceitos que foram alterados
    
      for i in  range(len(self.concept_coverage[self.material])):
        if(self.concept_coverage[self.material,i] == concept_coverage_neighbor[self.material,i]): #comparando se o material que foi alterado, está igual ao original ou se houve mudança
           if i in changed_concepts:
             del changed_concepts[changed_concepts.index(i)] #tirando dos changed concepts  os conceitos que foram alterados porem estão igual antes por multiplas alterações
      while(self.max_concepts_changes < len(changed_concepts) ): #revertendo conceitos que foram modificados e estão diferentes até o limitante
        selected_undo_concept_index = random.randrange(len(changed_concepts))
        concept_coverage_neighbor[self.material,changed_concepts[selected_undo_concept_index]] = ~concept_coverage_neighbor[self.material,changed_concepts[selected_undo_concept_index]]
        del changed_concepts[selected_undo_concept_index]

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
    cost_progress = []
    self.current_temperature = self.initial_temperature
    current_solution = concept_coverage

    current_fitness = fitnessConcepts_total
    
    self.get_orderOfModifiedMaterials()
    fitness_progress = []
    
    while(self.cost_counter < self.max_counter_fitness):
      for l in range(self.cycle):
        next_solution = self.get_randNeighbor(best_solution)
        next_fitness = self.counter_fitness(next_solution)
        self.deltaE = next_fitness - current_fitness
        
        if(self.deltaE < 0.0):
          current_solution = next_solution
          current_fitness = next_fitness
          
          if(next_fitness < best_fitness):
            best_solution = next_solution
            best_fitness = next_fitness
        else:
          if(random.uniform(0,1) < math.exp(-self.deltaE/self.current_temperature)):
            current_solution = next_solution
            current_fitness = next_fitness
        
        if(self.cost_counter>=self.max_counter_fitness):
          break
      
      self.current_temperature = self.decreaseTemperature(self.current_temperature)
      fitness_progress.append(best_fitness)
      cost_progress.append(self.cost_counter)
    print("counter:",self.cost_counter)  
    if(DATFILE):
      with open(DATFILE, 'w') as f:
        f.write(str(best_fitness))
    else:
      with open('results_SA.pickle', 'wb') as file:
        pickle.dump({"fitness_progress": fitness_progress, "sa_concept_coverage": best_solution, "sa_fitness": best_fitness,"cost_progress":cost_progress}, file)
        
      return best_solution, best_fitness

  def __repr__(self):
    return f'\n cycle: {self.cycle}\n initial_temperature: {self.initial_temperature}\n alpha: {self.alpha}\n max_materials_changes: {self.max_materials_changes}\n max_concepts_changes: {self.max_concepts_changes}\n seed: {self.seed}\n'

if __name__ == '__main__':
  ap = argparse.ArgumentParser(description='Simulated Annealing parameters definition')
  ap.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
  ap.add_argument('-cf',"--max_counter_fitness",type=int,default =3000,help="Cost limitation")
  ap.add_argument('-c', '--cycle', type=int, default=2, help='Number of cycles per temperature')
  ap.add_argument('-it', '--initial_temperature', default=1000.0, type=float,  help='Initial temperature')
  ap.add_argument('-a', '--alpha', type=float, default=0.90,  help='alpha')
  ap.add_argument('-b', '--beta', type=str,  default=0.2, help='beta')
  ap.add_argument('-mc','--max_materials_changes',default=10,help="max materials")
  ap.add_argument('-cc','--max_concepts_changes',default=5,help="max concepts")
  ap.add_argument('--datfile', dest='datfile', type=str, help='File where it will be save the score (result)')

  args = ap.parse_args()

  if args.verbose:
      logging.basicConfig(level=logging.DEBUG)

  logging.debug(args)
  
  student_results_before = sum([Fitness.get_fitnessConcepts(student_id, concept_coverage.T) for student_id in range(num_students)])/num_students
  
  
  simulatedAnnealing = SimulatedAnnealing(args.max_counter_fitness, args.cycle, args.initial_temperature, args.alpha, args.beta,args.max_materials_changes,args.max_concepts_changes,98092891)
  
  simulatedAnnealing.run(concept_coverage, student_results_before, args.datfile)
  # annealing_concept_coverage, student_results_annealing = simulatedAnnealing.run(concept_coverage, student_results_before)
  # print(f'student_results_annealing: {student_results_annealing}')