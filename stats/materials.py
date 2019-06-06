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

    show_general = False
    show_difficulty = False
    show_style = False
    show_concepts = True

    for (num, instance) in enumerate(instances):
        print(instance_list[num])
        print('=' * len(instance_list[num]))

        if show_general:
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

        if show_difficulty:
            print()
            print('Dificuldade')
            print('-----------')
            for difficulty in difficulty_list:
                mask = (instance.materials_difficulty == difficulty)
                num_materials = mask.sum()

                print('\n### Dificuldade %d:' % difficulty)
                print(' Número de materiais: %d'           % num_materials)
                print('Conceitos / material: %.2f +- %.2f' % (instance.concepts_materials[:, mask].sum() / num_materials, np.std(instance.concepts_materials[:, mask].sum(axis=0))))
                print('   Duração média (h): %.2f +- %.2f' % ((instance.estimated_time[mask] / 3600).mean(),              np.std(instance.estimated_time[mask] / 3600)))
                print('      Estilo act-ref: %s' % (np.histogram(instance.materials_active_reflexive[mask],  style_range)[0] / num_materials))
                print('      Estilo sen-int: %s' % (np.histogram(instance.materials_sensory_intuitive[mask], style_range)[0] / num_materials))
                print('      Estilo vis-ver: %s' % (np.histogram(instance.materials_visual_verbal[mask],     style_range)[0] / num_materials))
                print('      Estilo seq-glo: %s' % (np.histogram(instance.materials_sequential_global[mask], style_range)[0] / num_materials))

        if show_style:
            print()
            print('Estilo de aprendizado')
            print('---------------------')

            ati_mask = (instance.materials_active_reflexive < 0)
            ref_mask = (instance.materials_active_reflexive > 0)
            sen_mask = (instance.materials_sensory_intuitive < 0)
            int_mask = (instance.materials_sensory_intuitive > 0)
            vis_mask = (instance.materials_visual_verbal < 0)
            ver_mask = (instance.materials_visual_verbal > 0)
            seq_mask = (instance.materials_sequential_global < 0)
            glo_mask = (instance.materials_sequential_global > 0)

            print()
            print('|    __.__    |  <  |  0  |  >  |')
            print('|:-----------:|:---:|:---:|:---:|')
            print('| __ati-ref__ | %3d | %3d | %3d |' % (ati_mask.sum(), instance.num_materials - (ati_mask | ref_mask).sum(), ref_mask.sum()))
            print('| __sen-int__ | %3d | %3d | %3d |' % (sen_mask.sum(), instance.num_materials - (sen_mask | int_mask).sum(), int_mask.sum()))
            print('| __vis-ver__ | %3d | %3d | %3d |' % (vis_mask.sum(), instance.num_materials - (vis_mask | ver_mask).sum(), ver_mask.sum()))
            print('| __seq-glo__ | %3d | %3d | %3d |' % (seq_mask.sum(), instance.num_materials - (seq_mask | glo_mask).sum(), glo_mask.sum()))

            masks = []
            for atiref in (('ati', ati_mask), ('ref', ref_mask)):
                for senint in (('sen', sen_mask), ('int', int_mask)):
                    for visver in (('vis', vis_mask), ('ver', ver_mask)):
                        for seqglo in (('seq', seq_mask), ('glo', glo_mask)):
                            masks.append((atiref[0] + '-' + senint[0] + '-' + visver[0] + '-' + seqglo[0], (atiref[1] & senint[1] & visver[1] & seqglo[1]).sum()))

            print()
            print('|  __.__  | __ati__ | __ati__ | __ref__ | __ref__ |  __.__  |')
            print('|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|')
            print('| __sen__ |   %3d   |   %3d   |   %3d   |   %3d   | __seq__ |' % (masks[0][1], masks[2][1], masks[10][1], masks[8][1]))
            print('| __sen__ |   %3d   |   %3d   |   %3d   |   %3d   | __glo__ |' % (masks[1][1], masks[3][1], masks[11][1], masks[9][1]))
            print('| __int__ |   %3d   |   %3d   |   %3d   |   %3d   | __glo__ |' % (masks[5][1], masks[7][1], masks[15][1], masks[13][1]))
            print('| __int__ |   %3d   |   %3d   |   %3d   |   %3d   | __seq__ |' % (masks[4][1], masks[6][1], masks[14][1], masks[12][1]))
            print('|  __.__  | __vis__ | __ver__ | __ver__ | __vis__ |  __.__  |')

        if show_concepts:
            print()
            print('Conceitos')
            print('---------')

            print()
            print('|      Nome | nº materiais |')
            print('|----------:|--------------|')
            for num, concept in enumerate(instance.concepts_keys):
                print('| %9s | %12d |' % (concept, instance.concepts_materials[num].sum()))

        print()

    # test = np.array([-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6])
    # print(style_range)
    # print(test)
    # print(np.histogram(test, style_range)[0])
