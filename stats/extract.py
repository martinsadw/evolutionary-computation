from collections import defaultdict, Counter
import pickle

import numpy as np

from acs.instance import Instance


def extract_data(instance):
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
            # It may be faster to calculate which keys may have co-occurrence and only iterate on them
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

    quant_resource_types = np.array([len(material) for material in instance.materials_learning_resource_types])
    quant_resource_types_histogram = np.bincount(quant_resource_types)[1:]

    ############################################################################

    merged_resource_types = [resource for material in instance.materials_learning_resource_types for resource in material]
    resource_types_frequency = Counter(merged_resource_types)

    ############################################################################

    interactivity_level_frequency = Counter(instance.materials_interactivity_level)

    ############################################################################

    interactivity_type_frequency = Counter(instance.materials_interactivity_type)

    ############################################################################

    return {
        'instance': instance,
        'concepts_materials': instance.concepts_materials,
        'concepts_name': concepts_name,
        'concepts_quant': concepts_quant,
        'concepts_difficulty': concepts_difficulty,
        'count_histogram': count_histogram,
        'n_coocurrence_matrix': n_coocurrence_matrix,
        'coocurrence_set': coocurrence_set,
        'coocurrence_dict': coocurrence_dict,
        'quant_resource_types': quant_resource_types,
        'quant_resource_types_histogram': quant_resource_types_histogram,
        'resource_types_frequency': resource_types_frequency,
        'interactivity_level_frequency': interactivity_level_frequency,
        'interactivity_type_frequency': interactivity_type_frequency,
    }


if __name__ == '__main__':
    instance = Instance.load_from_file('instances/real/instance.txt')

    instance_data = extract_data(instance)

    with open('results/instance_stats.pickle', 'wb') as file:
        pickle.dump(instance_data, file)
