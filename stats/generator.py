import random

import numpy as np

from utils.roulette import roulette_spin


if __name__ == '__main__':
    num_materials = 1000
    new_concept_rate = 0.25

    concepts_name = [
          'ICHCC01',   'ICHCC02',   'ICHCC03',   'ICHCC04',   'ICHCC05',   'ICHCC06',
           'ICSN01',    'ICSN02',    'ICSN03',    'ICSN04',
            'ICL01',     'ICL02',     'ICL03',
           'ICFA01',    'ICFA02',    'ICFA03',
          'ICFBD01',   'ICFBD02',   'ICFBD03',
           'ICES01',    'ICES02',    'ICES03',
        'ICFSOOC01', 'ICFSOOC02', 'ICFSOOC03',
           'ICRC01',    'ICRC02',    'ICRC03',    'ICRC04',    'ICRC05',
    ]

    concepts_quant = [
        12, 11, 11, 11, 11, 9,
        18, 11, 14, 9,
        13, 15, 19,
        17, 15, 12,
        14, 12, 11,
        11, 12, 13,
        17, 12, 12,
        13, 16, 16, 12, 12,
    ]

    concepts_difficulty = [
        2.67, 2.73, 3.00, 3.27, 3.36, 2.22,
        3.06, 3.09, 2.86, 2.78,
        2.90, 2.53, 3.11,
        2.76, 2.73, 3.75,
        3.36, 3.25, 3.00,
        2.36, 2.50, 2.62,
        2.71, 2.83, 3.00,
        2.77, 2.81, 2.94, 3.00, 3.17,
    ]

    coocurrence_matrix = np.array([
        [12,  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 3, 11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0, 11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0, 11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0, 11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  9,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0, 18, 10,  9,  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0, 10, 11, 10,  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  9, 10, 14,  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  3,  3,  3,  9,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 15,  7,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  7, 19,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 17,  6,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  6, 15,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 12,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 14,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, 12,  2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2, 11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11,  8,  4,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  8, 12,  4,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4,  4, 13,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 17,  9,  1,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  9, 12,  1,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1, 12,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 13, 10,  9,  4,  3],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 10, 16, 10,  4,  3],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  9, 10, 16,  4,  3],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4,  4,  4, 12,  7],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  3,  3,  7, 12]
    ], dtype=float)
    coocurrence_matrix += 0.1  # Smoothing

    num_concepts = len(concepts_name)

    materials_list = []

    for i in range(num_materials):
        new_material = []

        remaining_concepts_name = concepts_name.copy()
        remaining_concepts_quant = concepts_quant.copy()

        concept_id = roulette_spin(remaining_concepts_quant)
        remaining_concepts_quant.pop(concept_id)
        new_name = remaining_concepts_name.pop(concept_id)
        # new_material.append(new_name)
        new_material.append(concept_id)

        while random.random() < new_concept_rate:
            concept_id = roulette_spin(remaining_concepts_quant)
            remaining_concepts_quant.pop(concept_id)
            new_name = remaining_concepts_name.pop(concept_id)
            # new_material.append(new_name)
            new_material.append(concept_id)

        materials_list.append(new_material)

    concepts_materials = np.zeros((num_concepts, num_materials))
    for j, material in enumerate(materials_list):
        for i in material:
            concepts_materials[i, j] = 1

    print(materials_list)
    print(concepts_materials.dot(concepts_materials.T))

    # a = np.empty((len(materials_list),))
    # for i, material in enumerate(materials_list):
    #     a[i] = len(material)
    #
    # print(np.sum(a))
    # print(np.mean(a))
    # print(np.std(a))
