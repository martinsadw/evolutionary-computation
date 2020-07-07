import csv
import math
import random

import numpy as np

from utils.roulette import Roulette, roulette_spin


def virtual_roulette(size, quant):
    combinations_size = (math.factorial(size) / math.factorial(size - quant))
    values_list = [*range(size)]

    combination_value = math.floor(random.random() * combinations_size)

    result = []
    for i in range(quant):
        result.append(values_list.pop(combination_value % (size - i)))
        combination_value //= (size - i)

    return result


def select_concepts(stats, quant, roulette_weight=1):
    num_concepts = len(stats['concepts_name'])
    concepts_quant = stats['concepts_quant']
    coocurrence_dict = stats['coocurrence_dict']

    if quant < 1:
        return []
    elif quant == 1:
        return [roulette_spin(concepts_quant)]
    else:
        coocurrence = coocurrence_dict[quant-2]

        coocurrence_keys = list(coocurrence.keys())
        coocurrence_values = [x.sum() for x in coocurrence.values()]
        coocurrence_quant = sum(coocurrence_values)

        roulette_quant = math.factorial(num_concepts) / (math.factorial(num_concepts - quant) * math.factorial(quant))

        roulette_value = random.random()
        # print("Chance: %d / (%d + %d) = %f" % (coocurrence_quant, coocurrence_quant, roulette_quant * roulette_weight, (coocurrence_quant / (coocurrence_quant + roulette_quant * roulette_weight))))
        # print("Valor: %f" % roulette_value)

        if roulette_value < 0.5:
        # if roulette_value < (coocurrence_quant / (coocurrence_quant + roulette_quant * roulette_weight)):
            selected_index = roulette_spin(coocurrence_values)
            return list(coocurrence_keys[selected_index])
        else:
            return virtual_roulette(num_concepts, quant)


def random_concepts_selector(stats, num_materials, mean_concepts, smoothing):
    concepts_quant = stats['concepts_quant']
    coocurrence_matrix = np.sum(stats['n_coocurrence_matrix'], axis=0) + smoothing
    num_concepts = len(stats['concepts_name'])
    new_concept_rate = 1 - (1 / mean_concepts)

    materials_list = []

    for i in range(num_materials):
        new_material = []

        remaining_concepts_id = list(range(num_concepts))

        concept_id = roulette_spin(concepts_quant)
        new_material.append(remaining_concepts_id.pop(concept_id))

        while random.random() < new_concept_rate and len(new_material) < num_concepts:
            new_probability = np.sum(coocurrence_matrix[new_material][:, remaining_concepts_id], axis=0)

            concept_id = roulette_spin(new_probability)
            new_material.append(remaining_concepts_id.pop(concept_id))

        materials_list.append(new_material)

    return materials_list


def histogram_concepts_selector(stats, num_materials, smoothing):
    concepts_quant = stats['concepts_quant']
    count_histogram = stats['count_histogram']
    coocurrence_matrix = np.sum(stats['n_coocurrence_matrix'], axis=0) + smoothing
    num_concepts = len(stats['concepts_name'])

    materials_list = []

    concept_roulette = Roulette(concepts_quant.astype(float))
    quant_roulette = Roulette(count_histogram.astype(float))

    for i in range(num_materials):
        new_material = []

        remaining_concepts_id = list(range(num_concepts))
        concept_id = concept_roulette.spin()
        new_material.append(remaining_concepts_id.pop(concept_id))

        quant_concepts = quant_roulette.spin() + 1
        for j in range(quant_concepts - 1):
            new_probability = np.sum(coocurrence_matrix[new_material][:, remaining_concepts_id], axis=0)

            concept_id = roulette_spin(new_probability)
            new_material.append(remaining_concepts_id.pop(concept_id))

        materials_list.append(new_material)

    return materials_list


def roulette_concepts_selector(stats, num_materials):
    count_histogram = stats['count_histogram']

    materials_list = []

    quant_roulette = Roulette(count_histogram.astype(float))

    for i in range(num_materials):
        quant_concepts = quant_roulette.spin() + 1

        materials_list.append(select_concepts(stats, quant_concepts))

    return materials_list


def write_material_coverage_file(filename, materials):
    with open(filename, 'w') as coverage_file:
        coverage_writer = csv.writer(coverage_file, delimiter=';')

        for i, material in enumerate(materials):
            coverage_writer.writerow([i] + material)
