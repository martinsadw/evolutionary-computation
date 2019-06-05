import pickle

import numpy as np

from acs.instance import Instance


if __name__ == '__main__':
    instance_list = [
    'instances/marcelo/instance_100.txt',
    'instances/marcelo/instance_200.txt',
    'instances/marcelo/instance_300.txt',
    'instances/real/instance.txt',
    # 'instances/test/instance_config.txt',
    ]

    difficulty_list = [1, 2, 3, 4, 5]
    style_range = np.arange(-6.5, 0, 3)
    # style_range = np.concatenate((style_range, -style_range[::-1]))
    style_range = np.concatenate((style_range, -style_range[::-1]))

    np.set_printoptions(precision=2)

    if False:
        instances = []
        for instance_file in instance_list:
            instances.append(Instance.load_from_file(instance_file))

        with open('results/instances.pickle', 'wb') as file:
            pickle.dump(instances, file)
    else:
        with open('results/instances.pickle', 'rb') as file:
            instances = pickle.load(file)

    for (num, instance) in enumerate(instances):
        print(instance_list[num])
        print('=' * len(instance_list[num]))
        print()
        print('Visão geral')
        print('-----------')
        print()
        print(' Número de materiais: %d'           % instance.num_materials)
        print(' Número de conceitos: %d'           % instance.num_concepts)
        print('   Média dificuldade: %.2f +- %.2f' % (np.mean(instance.materials_difficulty),                     np.std(instance.materials_difficulty)))
        print('Conceitos / material: %.2f +- %.2f' % (instance.concepts_materials.sum() / instance.num_materials, np.std(instance.concepts_materials.sum(axis=0))))
        print('   Duração total (h): %.2f'         % (instance.estimated_time / 3600).sum())
        print('   Duração média (h): %.2f +- %.2f' % ((instance.estimated_time / 3600).mean(),                    np.std(instance.estimated_time / 3600)))
        print('      Estilo act-ref: %s' % (np.histogram(instance.materials_active_reflexive,  style_range)[0] / instance.num_materials))
        print('      Estilo sen-int: %s' % (np.histogram(instance.materials_sensory_intuitive, style_range)[0] / instance.num_materials))
        print('      Estilo vis-ver: %s' % (np.histogram(instance.materials_visual_verbal,     style_range)[0] / instance.num_materials))
        print('      Estilo seq-glo: %s' % (np.histogram(instance.materials_sequential_global, style_range)[0] / instance.num_materials))
        print()
        print('Dificuldade')
        print('-----------')
        print()
        for difficulty in difficulty_list:
            mask = (instance.materials_difficulty == difficulty)
            num_materials = mask.sum()

            print('### Dificuldade %d:' % difficulty)
            print(' Número de materiais: %d'           % num_materials)
            print('Conceitos / material: %.2f +- %.2f' % (instance.concepts_materials[:, mask].sum() / num_materials, np.std(instance.concepts_materials[:, mask].sum(axis=0))))
            print('   Duração média (h): %.2f +- %.2f' % ((instance.estimated_time[mask] / 3600).mean(),              np.std(instance.estimated_time[mask] / 3600)))
            print('      Estilo act-ref: %s' % (np.histogram(instance.materials_active_reflexive[mask],  style_range)[0] / num_materials))
            print('      Estilo sen-int: %s' % (np.histogram(instance.materials_sensory_intuitive[mask], style_range)[0] / num_materials))
            print('      Estilo vis-ver: %s' % (np.histogram(instance.materials_visual_verbal[mask],     style_range)[0] / num_materials))
            print('      Estilo seq-glo: %s' % (np.histogram(instance.materials_sequential_global[mask], style_range)[0] / num_materials))
            print()
        print()

    # test = np.array([-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6])
    # print(style_range)
    # print(test)
    # print(np.histogram(test, style_range)[0])
