from numpy.core.fromnumeric import sort
from pandas.io.parsers import count_empty_vals
from acs.course import Course
import pickle
import pandas as pd
import csv
import numpy as np
from config import instance
from acs.instance import Instance
import os
from fitness import Fitness
from config import instance, concept_coverage, objectives, num_students, num_concepts, num_materials, recommendation
from algorithms import simulated_annealing

class New_material_coverage():
    def __init__(self) -> None:
        
        self.best_solution_sa = pickle.load(open('/mnt/c/Users/fonse/Documents/Improving-LOR/results_SA.pickle','rb'))["sa_concept_coverage"]
        self.best_solution_grasp = pickle.load(open('/mnt/c/Users/fonse/Documents/Improving-LOR/results_grasp_best.pickle','rb'))["grasp_concept_coverage"]
        self.concepts_csv = pd.read_csv('/mnt/c/Users/fonse/Documents/Improving-LOR/instances/real/concepts.csv',delimiter= ';',header=None)
        self.course = Course('/mnt/c/Users/fonse/Documents/Improving-LOR/instances/real/instance.txt')
        self.concepts_keys = sorted(self.course.concepts.keys())


    def get_new_material_coverage(self,best_solution):
        material_coverage = {}
        for i in range(len(best_solution)):
            concepts = []
            for j in range(len(best_solution[i])):
                if(best_solution[i][j] == True):
                    concepts.append(self.concepts_keys[j])
            material_coverage[i] = concepts

        return material_coverage            

    def get_concept_coverage_grasp(self):
        with  open('/mnt/c/Users/fonse/Documents/Improving-LOR/new_material_coverage/material_coverage_grasp.csv','w') as file:
            writer = csv.writer(file,delimiter = ';')
            for key, value in self.get_new_material_coverage(self.best_solution_grasp).items():
                writer.writerow([key] + value)

    def get_concept_coverage_sa(self):
        with  open('/mnt/c/Users/fonse/Documents/Improving-LOR/new_material_coverage/material_coverage_sa.csv','w') as file:
            writer = csv.writer(file,delimiter = ';')
            for key, value in self.get_new_material_coverage(self.best_solution_sa).items():
                writer.writerow([key] + value)


new_material = New_material_coverage()
new_material.get_concept_coverage_sa()

materials_changed = 0
materials_changed_index = []
for i in range(len(new_material.best_solution_sa)):
    if sum(new_material.best_solution_sa[i] != instance.concepts_materials.T[i]) > 0:
        materials_changed = materials_changed +1
        materials_changed_index.append(i)

print(materials_changed)      
print(materials_changed_index)

add_concepts = []
cont_concept = 0
for i in range(len(new_material.best_solution_sa)):

    old_concepts = sum(instance.concepts_materials.T[i] == True)
    new_concepts = sum(new_material.best_solution_sa[i] == True)

    if ( new_concepts > old_concepts):
        
        add_concepts.append(i)

print(add_concepts)       


fitness = sum([Fitness.get_fitnessConcepts(student_id, new_material.best_solution_sa.T) for student_id in range(num_students)])/num_students        
print(fitness)

teste_concepts_materials = instance.concepts_materials.T.copy()
for i in range(len(teste_concepts_materials)):
    teste_concepts_materials[i] = [True if x==False else x for x in teste_concepts_materials[i]]

fitness_teste = sum([Fitness.get_fitnessConcepts(student_id, teste_concepts_materials.T) for student_id in range(num_students)])/num_students        
print(fitness_teste)


sa_results = pickle.load( open( "/mnt/c/Users/fonse/Documents/Improving-LOR/results_SA.pickle", "rb" ) )
teste = sa_results['concept_mask']

print(teste[40])
#print(instance.concepts_materials.T[1])