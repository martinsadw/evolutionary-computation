import math
import pickle
import random

import numpy as np
import matplotlib.pyplot as plt

from utils.roulette import Roulette, roulette_spin
from generator.concepts_selector import random_concepts_selector, histogram_concepts_selector, roulette_concepts_selector


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

    gen_type = 2
    if gen_type == 0:
        materials_list = random_concepts_selector(stats, num_materials, mean_concepts, smoothing)

    elif gen_type == 1:
        materials_list = histogram_concepts_selector(stats, num_materials, smoothing)

    elif gen_type == 2:
        materials_list = roulette_concepts_selector(stats, num_materials)

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
