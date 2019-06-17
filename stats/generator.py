import random
import pickle

import numpy as np
import matplotlib.pyplot as plt

from utils.roulette import Roulette, roulette_spin


if __name__ == '__main__':
    ############################################################################
    num_materials = 10000
    mean_concepts = 1.33
    smoothing = 0.01
    ############################################################################
    with open('results/instance_stats.pickle', 'rb') as file:
        stats = pickle.load(file)

    concepts_name = stats['concepts_name']
    concepts_quant = stats['concepts_quant']
    concepts_difficulty = stats['concepts_difficulty']
    coocurrence_matrix = np.sum(stats['n_coocurrence_matrix'], axis=0)
    count_histogram = stats['count_histogram']

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

    concepts_materials = np.zeros((num_concepts, num_materials), dtype=int)
    for j, material in enumerate(materials_list):
        for i in material:
            concepts_materials[i, j] = 1

    new_coocurences_matrix = concepts_materials.dot(concepts_materials.T)
    quant_concepts = np.sum(concepts_materials, axis=0)

    print(np.sum(quant_concepts))
    print(np.mean(quant_concepts))
    print(np.std(quant_concepts))

    concepts_count = concepts_materials.sum(axis=0)
    count_histogram = np.bincount(concepts_count)
    print(count_histogram / count_histogram.sum())
    # for i in range(count_histogram.shape[0]):
    #     count_mask = (concepts_count == i)
    #
    #     int_concepts_materials = concepts_materials[:, count_mask].astype(int)
    #     coocurrence = int_concepts_materials.dot(int_concepts_materials.T)
    #     print("-%d-------------------------------------------" % i)
    #     print(coocurrence)
    #     print("---------------------------------------------")

    fig = plt.figure()
    fig.suptitle('Matriz de coocorrência - Sintética - Suavização %.2f' % smoothing)
    plt.imshow(new_coocurences_matrix, interpolation='nearest', cmap='gray')
    plt.colorbar()
    plt.show()

    fig = plt.figure()
    fig.suptitle('Matriz de coocorrência - Real')
    plt.imshow(coocurrence_matrix, interpolation='nearest', cmap='gray')
    plt.colorbar()
    plt.show()
