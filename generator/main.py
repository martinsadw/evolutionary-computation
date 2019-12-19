import math
import pickle
import random

import numpy as np
import matplotlib.pyplot as plt

from utils.roulette import Roulette
from generator.concepts_selector import random_concepts_selector, histogram_concepts_selector, roulette_concepts_selector, write_material_coverage_file
from generator.lom import write_lom_file


if __name__ == '__main__':
    ############################################################################
    num_materials = 284
    mean_concepts = 1.33
    smoothing = 0.01
    ############################################################################
    with open('results/instance_stats.pickle', 'rb') as file:
        stats = pickle.load(file)

    concepts_materials = stats['concepts_materials']
    concepts_name = stats['concepts_name']
    concepts_quant = stats['concepts_quant']
    concepts_difficulty = stats['concepts_difficulty']
    coocurrence_matrix = np.sum(stats['n_coocurrence_matrix'], axis=0)
    count_histogram = stats['count_histogram']
    coocurrence_set = stats['coocurrence_set']
    coocurrence_dict = stats['coocurrence_dict']

    num_concepts = len(concepts_name)
    new_concept_rate = 1 - (1 / mean_concepts)
    coocurrence_matrix += smoothing
    ############################################################################

    gen_type = 2
    if gen_type == 0:
        materials_list = random_concepts_selector(stats, num_materials, mean_concepts, smoothing)

    elif gen_type == 1:
        materials_list = histogram_concepts_selector(stats, num_materials, smoothing)

    elif gen_type == 2:
        materials_list = roulette_concepts_selector(stats, num_materials)

    materials_list = [sorted(material) for material in materials_list]
    materials_list = [[concepts_name[concept] for concept in material] for material in sorted(materials_list)]
    write_material_coverage_file('results/material_coverage.csv', materials_list)

    difficulty_roulette = Roulette([16, 72, 130, 48, 18])
    materials_difficulty = np.empty((num_materials,), dtype=int)
    materials_duration = np.empty((num_materials,), dtype=int)
    for i in range(num_materials):
        materials_difficulty[i] = difficulty_roulette.spin() + 1

        if materials_difficulty[i] == 1:
            max_indice = 16
            power_a = 36.74891727
            power_b = 1.23339668
        if materials_difficulty[i] == 2:
            max_indice = 72
            power_a = 31.44068961
            power_b = 0.954634698
        if materials_difficulty[i] == 3:
            max_indice = 130
            power_a = 22.37523474
            power_b = 1.021917379
        if materials_difficulty[i] == 4:
            max_indice = 48
            power_a = 80.7756257
            power_b = 0.904543376
        if materials_difficulty[i] == 5:
            max_indice = 18
            power_a = 103.7746477
            power_b = 1.531354033

        power_x = (random.random() * max_indice) + 1
        materials_duration[i] = int(power_a * power_x ** power_b)

    materials_active_reflexive  = np.round(np.random.normal(-2.32, 1.54, size=(num_materials,)))
    materials_sensory_intuitive = np.round(np.random.normal(-0.36, 1.12, size=(num_materials,)))
    materials_visual_verbal     = np.round(np.random.normal( 0.34, 0.90, size=(num_materials,)))
    materials_sequential_global = np.round(np.random.normal(-0.52, 0.76, size=(num_materials,)))

    write_lom_file()

    # Estilo act-ref: -2.32 +- 1.54
    # Estilo sen-int: -0.36 +- 1.12
    # Estilo vis-ver:  0.34 +- 0.90
    # Estilo seq-glo: -0.52 +- 0.76
