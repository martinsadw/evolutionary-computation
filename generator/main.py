import math
import pickle
import random

import numpy as np
import matplotlib.pyplot as plt

from utils.roulette import Roulette, roulette_spin
from generator.concepts_selector import random_concepts_selector, histogram_concepts_selector, roulette_concepts_selector, write_material_coverage_file


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

    for material in materials_list:
        difficulty = random.randint(1, 5)

        if difficulty == 1:
            max_indice = 16
            power_a = 36.74891727
            power_b = 1.23339668
        if difficulty == 2:
            max_indice = 72
            power_a = 31.44068961
            power_b = 0.954634698
        if difficulty == 3:
            max_indice = 130
            power_a = 22.37523474
            power_b = 1.021917379
        if difficulty == 4:
            max_indice = 48
            power_a = 80.7756257
            power_b = 0.904543376
        if difficulty == 5:
            max_indice = 18
            power_a = 103.7746477
            power_b = 1.531354033

        power_x = (random.random() * max_indice) + 1
        material_duration = int(power_a * power_x ** power_b)

        print(difficulty, material_duration)
