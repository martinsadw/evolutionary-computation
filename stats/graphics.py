import pickle
from pprint import pprint

import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    with open('results/instance_stats.pickle', 'rb') as file:
        stats = pickle.load(file)

    base_folder = 'results/2019-10-17 - Caracteristicas da base'

    ############################################################################
    # Dificuldade
    ############################################################################
    fig = plt.figure()
    fig.suptitle('Histograma de dificuldade')
    difficulty_histogram = np.bincount(stats['instance'].materials_difficulty)[1:]
    plt.bar(np.arange(len(difficulty_histogram)), difficulty_histogram, width=0.9)
    plt.savefig(base_folder + '/difficulty.png')
    # plt.show()
    ############################################################################

    ############################################################################
    # Duração
    ############################################################################
    fig = plt.figure()
    fig.suptitle('Histograma de duração')
    plt.hist(stats['instance'].estimated_time / 3600, bins=200)
    plt.savefig(base_folder + '/time.png')
    # plt.show()
    ############################################################################

    ############################################################################
    # Duração por dificuldade
    ############################################################################
    fig = plt.figure(figsize=(10, 8))
    fig.suptitle('Histograma de duração')
    for difficulty in [1, 2, 3, 4, 5]:
        mask = (stats['instance'].materials_difficulty == difficulty)

        plt.subplot(3, 2, difficulty)
        plt.ylabel('Dificuldade %d' % difficulty)
        plt.ylim((0, 3))
        plt.hist(stats['instance'].estimated_time[mask] / 3600, bins=50, range=(0, 14), density=True)

    plt.subplot(3, 2, 6)
    plt.ylabel('Geral')
    plt.ylim((0, 3))
    plt.hist(stats['instance'].estimated_time / 3600, bins=50, range=(0, 14), density=True)
    plt.savefig(base_folder + '/time_per_difficulty.png')
    # plt.show()
    ############################################################################


    ############################################################################
    # Quantidade de conceitos
    ############################################################################
    fig = plt.figure()
    fig.suptitle('Histograma de quantidade de conceitos')
    plt.bar(np.arange(len(stats['count_histogram'])), stats['count_histogram'], width=0.9)
    plt.savefig(base_folder + '/number_concepts.png')
    # plt.show()
    ############################################################################

    styles = [
        ('active_reflexive', 'ativo - reflexivo', stats['instance'].materials_active_reflexive),
        ('sensory_intuitive', 'sensorial - intuitivo', stats['instance'].materials_sensory_intuitive),
        ('visual_verbal', 'visual - verbal', stats['instance'].materials_visual_verbal),
        ('sequential_global', 'sequencial - global', stats['instance'].materials_sequential_global),
    ]
    ############################################################################
    # Estilo de aprendizado
    ############################################################################
    for (style_filename, style_name, style_axis) in styles:
        fig = plt.figure()
        fig.suptitle('Histograma de estilo %s' % style_name)
        plt.hist(style_axis, bins=11, range=(-5, 6), rwidth=0.9)
        plt.savefig(base_folder + '/style_%s.png' % style_filename)
        # plt.show()
    ############################################################################

    ############################################################################
    # Duração por dificuldade
    ############################################################################
    for (style_filename, style_name, style_axis) in styles:
        fig = plt.figure(figsize=(10, 8))
        fig.suptitle('Histograma de estilo %s' % style_name)
        for difficulty in [1, 2, 3, 4, 5]:
            mask = (stats['instance'].materials_difficulty == difficulty)

            plt.subplot(3, 2, difficulty)
            plt.ylabel('Dificuldade %d' % difficulty)
            plt.ylim((0, 0.6))
            plt.hist(style_axis[mask], bins=11, range=(-5, 6), density=True, rwidth=0.9)

        plt.subplot(3, 2, 6)
        plt.ylabel('Geral')
        plt.ylim((0, 0.6))
        plt.hist(style_axis, bins=11, range=(-5, 6), density=True, rwidth=0.9)
        plt.savefig(base_folder + '/style_%s_per_difficulty.png' % style_filename)
        # plt.show()
    ############################################################################
