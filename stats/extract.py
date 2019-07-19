from collections import defaultdict
import pickle

import numpy as np

from acs.instance import Instance


if __name__ == '__main__':
    instance = Instance.load_from_file('instances/real/instance.txt')

    concepts_name = instance.concepts_keys

    num_concepts = len(concepts_name)

    ############################################################################

    concepts_quant = np.sum(instance.concepts_materials, axis=1)
    concepts_quant[concepts_quant == 0] = round(np.mean(concepts_quant[concepts_quant != 0]))

    ############################################################################

    concepts_difficulty = np.empty((num_concepts,))
    for num, concept in enumerate(instance.concepts_keys):
        concept_mask = instance.concepts_materials[num]
        num_materials = concept_mask.sum()

        if num_materials == 0:
            concepts_difficulty[num] = 0
        else:
            concepts_difficulty[num] = np.mean(instance.materials_difficulty[concept_mask])
    concepts_difficulty[concepts_difficulty == 0] = np.mean(instance.materials_difficulty)

    ############################################################################

    int_concepts_materials = instance.concepts_materials.astype(int)
    coocurrence_matrix = int_concepts_materials.dot(int_concepts_materials.T)

    concepts_count = instance.concepts_materials.sum(axis=0)
    count_histogram = np.bincount(concepts_count)[1:]

    ############################################################################

    n_coocurrence_matrix = np.empty((count_histogram.shape[0], num_concepts, num_concepts))
    for i in range(count_histogram.shape[0]):
        count_mask = (concepts_count == (i + 1))

        int_concepts_materials = instance.concepts_materials[:, count_mask].astype(int)
        n_coocurrence_matrix[i] = int_concepts_materials.dot(int_concepts_materials.T)

    ############################################################################

    coocurrence_set = []
    coocurrence_dict = []

    coocurrence_set.append(defaultdict(set))
    coocurrence_dict.append({})
    for i in range(num_concepts):
        for j in range(i+1, num_concepts):
            concept_and = instance.concepts_materials[i] & instance.concepts_materials[j]
            if concept_and.sum() > 0:
                coocurrence_set[0][i].add(j)
                coocurrence_set[0][j].add(i)
                coocurrence_dict[0][frozenset([i, j])] = concept_and

    while (len(coocurrence_dict[-1]) > 0):
        current_set = defaultdict(set)
        current_dict = {}
        for (key, value) in coocurrence_dict[-1].items():
            # Talvez seja mais rapido calcular quais são as chaves que podem ter coocorrencia
            # possible_keys = set.intersection(*[coocurrence_set[0][x] for x in key])

            for i in range(num_concepts):
                if i not in key:
                    if key.union([i]) in current_dict:
                        current_set[key].add(i)
                    else:
                        concept_and = value & instance.concepts_materials[i]
                        if concept_and.sum() > 0:
                            current_set[key].add(i)
                            current_dict[key.union([i])] = concept_and

        coocurrence_set.append(current_set)
        coocurrence_dict.append(current_dict)

    ############################################################################

    with open('results/instance_stats.pickle', 'wb') as file:
        pickle.dump({
            'concepts_materials': instance.concepts_materials,
            'concepts_name': concepts_name,
            'concepts_quant': concepts_quant,
            'concepts_difficulty': concepts_difficulty,
            'count_histogram': count_histogram,
            'n_coocurrence_matrix': n_coocurrence_matrix,
            'coocurrence_set': coocurrence_set,
            'coocurrence_dict': coocurrence_dict,
        }, file)
