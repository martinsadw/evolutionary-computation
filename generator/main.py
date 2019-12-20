import math
import pickle
import random

import numpy as np
import matplotlib.pyplot as plt

from utils.roulette import Roulette, roulette_spin
from generator.concepts_selector import random_concepts_selector, histogram_concepts_selector, roulette_concepts_selector, write_material_coverage_file
from generator.lom import write_lom_file

from acs.instance import Instance


def time_to_string(time):
    result = 'PT'
    if (time > 60 * 60):
        result += str(time // (60 * 60)) + 'H'
        time = time % (60 * 60)
    if (time > 60):
        result += str(time // 60) + 'M'
        time = time % 60

    result += str(time) + 'S'

    return result


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
    quant_resource_types = stats['quant_resource_types']
    quant_resource_types_histogram = stats['quant_resource_types_histogram']
    resource_types_frequency = stats['resource_types_frequency']

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
    quant_resource_types_roulette = Roulette(quant_resource_types_histogram.tolist())

    resource_types_name = list(resource_types_frequency.keys())
    resource_types_frequency_values = list(resource_types_frequency.values())

    materials_difficulty = np.empty((num_materials,), dtype=int)
    materials_duration = np.empty((num_materials,), dtype=int)
    materials_resource_types = [None] * num_materials
    for i in range(num_materials):
        materials_difficulty[i] = difficulty_roulette.spin() + 1

        if materials_difficulty[i] == 1:
            max_indice = 16
            power_a = 68.12307258
            power_b = 0.2095535293
        if materials_difficulty[i] == 2:
            max_indice = 72
            power_a = 134.6334519
            power_b = 0.04677506963
        if materials_difficulty[i] == 3:
            max_indice = 130
            power_a = 175.1923166
            power_b = 0.0293693865
        if materials_difficulty[i] == 4:
            max_indice = 48
            power_a = 106.7568341
            power_b = 0.09490106732
        if materials_difficulty[i] == 5:
            max_indice = 18
            power_a = 84.89245786
            power_b = 0.3313514637

        power_x = (random.random() * max_indice) + 1
        materials_duration[i] = int(power_a * math.e ** (power_b * power_x))

        material_quant_resource_types = quant_resource_types_roulette.spin() + 1
        materials_resource_types[i] = []
        remaining_resource_types = resource_types_name.copy()
        remaining_resource_types_frequency = resource_types_frequency_values.copy()
        for j in range(material_quant_resource_types):
            new_resource_type_index = roulette_spin(remaining_resource_types_frequency)

            materials_resource_types[i].append(remaining_resource_types[new_resource_type_index])
            del remaining_resource_types[new_resource_type_index]
            del remaining_resource_types_frequency[new_resource_type_index]

    difficulty_strings = ['none', 'very easy', 'easy', 'medium', 'difficult', 'very difficult']

    interactivity_type = ['mixed'] * num_materials
    interactivity_level = ['low'] * num_materials
    learning_resource_types = materials_resource_types
    difficulty = [difficulty_strings[difficulty_values] for difficulty_values in materials_difficulty]
    typical_learning_time = [time_to_string(duration_values) for duration_values in materials_duration]

    write_lom_file(interactivity_type, interactivity_level, learning_resource_types, difficulty, typical_learning_time)

    # Estilo act-ref: -2.32 +- 1.54
    # Estilo sen-int: -0.36 +- 1.12
    # Estilo vis-ver:  0.34 +- 0.90
    # Estilo seq-glo: -0.52 +- 0.76
