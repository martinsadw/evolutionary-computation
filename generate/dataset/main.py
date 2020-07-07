import math
import pickle
import random
from collections import namedtuple

import numpy as np
import matplotlib.pyplot as plt

from utils.roulette import Roulette, roulette_spin
from generate.dataset.concepts_selector import random_concepts_selector, histogram_concepts_selector, roulette_concepts_selector, write_material_coverage_file
from generate.dataset.lom import write_lom_file

from acs.instance import Instance


_difficulty_strings = ['none', 'very easy', 'easy', 'medium', 'difficult', 'very difficult']


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


def generate_materials(stats, num_materials, gen_type, args):
    concepts_name = stats['concepts_name']
    quant_resource_types_histogram = stats['quant_resource_types_histogram']
    resource_types_frequency = stats['resource_types_frequency']
    interactivity_level_frequency = stats['interactivity_level_frequency']
    interactivity_type_frequency = stats['interactivity_type_frequency']

    if gen_type == 'random':
        materials_list = random_concepts_selector(stats, num_materials, args.mean_concepts, args.smoothing)

    elif gen_type == 'histogram':
        materials_list = histogram_concepts_selector(stats, num_materials, args.smoothing)

    elif gen_type == 'roulette':
        materials_list = roulette_concepts_selector(stats, num_materials)

    materials_list = [sorted(material) for material in materials_list]
    # materials_list = [[concepts_name[concept] for concept in material] for material in sorted(materials_list)]
    materials_list = [[concepts_name[concept] for concept in material] for material in materials_list]

    difficulty_roulette = Roulette([16, 72, 130, 48, 18])
    quant_resource_types_roulette = Roulette(quant_resource_types_histogram.tolist())

    resource_types_name = list(resource_types_frequency.keys())
    resource_types_frequency_values = list(resource_types_frequency.values())

    interactivity_type_name = list(interactivity_type_frequency.keys())
    interactivity_type_frequency_values = list(interactivity_type_frequency.values())
    interactivity_type_frequency_roulette = Roulette(interactivity_type_frequency_values)

    interactivity_level_name = list(interactivity_level_frequency.keys())
    interactivity_level_frequency_values = list(interactivity_level_frequency.values())
    interactivity_level_frequency_roulette = Roulette(interactivity_level_frequency_values)

    materials_difficulty = np.empty((num_materials,), dtype=int)
    materials_duration = np.empty((num_materials,), dtype=int)
    materials_resource_types = [None] * num_materials
    materials_interactivity_type = [None] * num_materials
    materials_interactivity_level = [None] * num_materials
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

        materials_interactivity_type[i] = interactivity_type_name[interactivity_type_frequency_roulette.spin()]
        materials_interactivity_level[i] = interactivity_level_name[interactivity_level_frequency_roulette.spin()]

    interactivity_type = materials_interactivity_type
    interactivity_level = materials_interactivity_level
    learning_resource_types = materials_resource_types
    difficulty = [_difficulty_strings[difficulty_values] for difficulty_values in materials_difficulty]
    typical_learning_time = [time_to_string(duration_values) for duration_values in materials_duration]

    lom_data = {
        'interactivity_type': interactivity_type,
        'interactivity_level': interactivity_level,
        'learning_resource_types': learning_resource_types,
        'difficulty': difficulty,
        'typical_learning_time': typical_learning_time,
    }

    return (materials_list, lom_data)

if __name__ == '__main__':
    num_materials = 1000
    gen_type = 'roulette'
    mean_concepts = 1.33
    smoothing = 0.01

    with open('results/instance_stats.pickle', 'rb') as file:
        stats = pickle.load(file)

    Args = namedtuple('Args', ['mean_concepts', 'smoothing'])
    args = Args(mean_concepts=mean_concepts, smoothing=smoothing)
    (materials_list, lom_data) = generate_materials(stats, num_materials, gen_type, args)

    write_material_coverage_file('results/material_coverage.csv', materials_list)
    write_lom_file('results/LOMs', lom_data)
