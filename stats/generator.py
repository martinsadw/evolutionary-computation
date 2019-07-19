import random
import pickle
import math

import numpy as np
import matplotlib.pyplot as plt

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


if __name__ == '__main__':
    ############################################################################
    num_materials = 10000
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

    materials_list = []

    gen_type = 1
    if gen_type == 0:
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
    elif gen_type == 1:
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
    elif gen_type == 2:
        quant_roulette = Roulette(count_histogram.astype(float))

        for i in range(num_materials):
            quant_concepts = quant_roulette.spin() + 1

            materials_list.append(select_concepts(stats, quant_concepts))

    new_concepts_materials = np.zeros((num_concepts, num_materials), dtype=int)
    for j, material in enumerate(materials_list):
        for i in material:
            new_concepts_materials[i, j] = 1

    new_coocurences_matrix = new_concepts_materials.dot(new_concepts_materials.T)
    quant_concepts = np.sum(new_concepts_materials, axis=0)

    print(np.sum(quant_concepts))
    print(np.mean(quant_concepts))
    print(np.std(quant_concepts))

    concepts_count = new_concepts_materials.sum(axis=0)
    count_histogram = np.bincount(concepts_count)
    print(count_histogram / count_histogram.sum())

    # fig = plt.figure()
    # fig.suptitle('Matriz de coocorrência - Sintética - Suavização %.2f' % smoothing)
    # plt.imshow(new_coocurences_matrix, interpolation='nearest', cmap='gray')
    # plt.colorbar()
    # plt.show()
    #
    # fig = plt.figure()
    # fig.suptitle('Matriz de coocorrência - Real')
    # plt.imshow(coocurrence_matrix, interpolation='nearest', cmap='gray')
    # plt.colorbar()
    # plt.show()
