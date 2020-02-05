import pickle
from pprint import pprint

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

font = {'size': 14}
mpl.rc('font', **font)

use_grayscale = False
if use_grayscale:
    suffix = "_pb"
    cmap = 'gray'
    color = ['k']
    graphics_cycler = (cycler('color', color) * cycler('marker', ['.', '^', 'd', 'x', '*']) * cycler('linestyle', ['-', '--']))
else:
    suffix = ""
    cmap = 'viridis'
    color = ['#1f77b4']
    graphics_cycler = cycler('color', ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
# mpl.rcParams['axes.prop_cycle'] = graphics_cycler

format = "pdf"

if __name__ == '__main__':
    with open('results/instance_stats.pickle', 'rb') as file:
        stats = pickle.load(file)

    base_folder = 'results/2020-01-24 - Gráficos artigo'

    ############################################################################
    # Dificuldade
    ############################################################################
    # fig = plt.figure()
    fig, ax = plt.subplots()
    ax.set_prop_cycle(graphics_cycler)
    # fig.suptitle('Histograma de dificuldade')
    plt.ylabel('# materials')
    plt.xlabel('Difficulty')
    difficulty_histogram = np.bincount(stats['instance'].materials_difficulty)[1:]
    plt.bar(np.arange(len(difficulty_histogram)) + 1, difficulty_histogram, width=0.9)
    plt.savefig(base_folder + '/difficulty%s.%s' % (suffix, format))
    plt.close()
    # plt.show()

    # fig = plt.figure()
    # # fig.suptitle('Histograma de dificuldade')
    # plt.ylabel('# materials')
    # plt.xlabel('Difficulty')
    # difficulty_histogram = np.bincount(stats['instance'].materials_difficulty)[1:]
    # plt.plot(np.arange(len(difficulty_histogram)) + 1, difficulty_histogram)
    # plt.savefig(base_folder + '/difficulty_line%s.%s' % (suffix, format))
    # plt.close()
    # # plt.show()
    ############################################################################

    ############################################################################
    # Duração
    ############################################################################
    # fig = plt.figure()
    # fig.suptitle('Histograma de duração')
    # plt.hist(stats['instance'].estimated_time / 3600, bins=200)
    # plt.savefig(base_folder + '/time%s.%s' % (suffix, format))
    # # plt.show()
    ############################################################################

    ############################################################################
    # Duração por dificuldade
    ############################################################################
    # fig = plt.figure(figsize=(10, 8))
    # fig = plt.figure()
    fig, ax = plt.subplots()
    ax.set_prop_cycle(graphics_cycler)
    # fig.suptitle('Histograma de duração')
    plt.ylabel('Duration (h)')
    plt.xlabel('Normalized index')
    # plt.ylim((0, 3))

    markersize = [2, 5, 10, 5, 2]

    for difficulty in [1, 2, 3, 4, 5]:
        mask = (stats['instance'].materials_difficulty == difficulty)

        materials_duration = sorted(stats['instance'].estimated_time[mask] / 3600)
        quant_materials = len(materials_duration)
        # plt.plot(np.arange(quant_materials) / (quant_materials - 1), materials_duration, markersize=5, markevery=markersize[difficulty-1], label=("Difficulty %d" % difficulty))
        plt.semilogy(np.arange(quant_materials) / (quant_materials - 1), materials_duration, markersize=5, markevery=markersize[difficulty-1], label=("Difficulty %d" % difficulty))

    plt.legend(loc=2)
    plt.savefig(base_folder + '/time_per_difficulty%s.%s' % (suffix, format))
    plt.close()
    # plt.show()
    ############################################################################


    ############################################################################
    # Quantidade de conceitos
    ############################################################################
    # fig = plt.figure()
    fig, ax = plt.subplots()
    ax.set_prop_cycle(graphics_cycler)
    # fig.suptitle('Histograma de quantidade de conceitos')
    plt.ylabel('# materials')
    plt.xlabel('# concepts')
    plt.bar(np.arange(len(stats['count_histogram'])) + 1, stats['count_histogram'], width=0.9)
    plt.savefig(base_folder + '/number_concepts%s.%s' % (suffix, format))
    plt.close()
    # plt.show()
    ############################################################################

    styles = [
        (0, 'active_reflexive', 'reflective - active', stats['instance'].materials_active_reflexive),
        (1, 'sensory_intuitive', 'intuitive - sensing', stats['instance'].materials_sensory_intuitive),
        (2, 'visual_verbal', 'verbal - visual', stats['instance'].materials_visual_verbal),
        (3, 'sequential_global', 'global - sequencial', stats['instance'].materials_sequential_global),
    ]
    ############################################################################
    # Estilo de aprendizado
    ############################################################################
    fig = plt.figure()
    fig, ax = plt.subplots()
    ax.set_prop_cycle(graphics_cycler)
    # fig.suptitle('Histograma de estilo %s' % style_name)
    plt.ylabel('# materials')
    plt.xlabel('Dimension value')
    plt.ylim((-10, 200))

    styles_map = np.empty((4, 13))
    for (i, style_filename, style_name, style_axis) in styles:
        style_histogram = np.histogram(style_axis, bins=13, range=(-6, 7))
        styles_map[i] = style_histogram[0]
        plt.plot(style_histogram[1][:-1], style_histogram[0], label=style_name)
        # plt.bar(style_histogram[1][:-1] + ((i-1.5) * 0.2), style_histogram[0], width=0.2, label=style_name)

    plt.legend(loc=1)
    plt.savefig(base_folder + '/style%s.%s' % (suffix, format))
    plt.close()
    # plt.show()

    # styles_map = np.stack((styles[0][3], styles[1][3], styles[2][3], styles[3][3]))
    print(styles_map)
    fig, ax = plt.subplots()
    im = ax.imshow(styles_map, cmap=cmap)
    fig.subplots_adjust(left=0.25)
    fig.colorbar(im, orientation="horizontal", aspect=40)
    ax.set_xticks(np.arange(0, 13)[::2])
    ax.set_xticklabels(np.arange(-6, 7)[::2])
    ax.set_yticks(range(4))
    ax.set_yticklabels(["Processing", "Perception", "Input", "Understanding"])
    ax.text(0, 0, "Reflexive", ha="left", va="center", color="w")
    ax.text(12, 0, "Active", ha="right", va="center", color="w")
    ax.text(0, 1, "Intuitive", ha="left", va="center", color="w")
    ax.text(12, 1, "Sensing", ha="right", va="center", color="w")
    ax.text(0, 2, "Verbal", ha="left", va="center", color="w")
    ax.text(12, 2, "Visual", ha="right", va="center", color="w")
    ax.text(0, 3, "Global", ha="left", va="center", color="w")
    ax.text(12, 3, "Sequencial", ha="right", va="center", color="w")
    plt.savefig(base_folder + '/style_map%s.%s' % (suffix, format))
    plt.close()
    # plt.show()
    ############################################################################

    ############################################################################
    # Estilo de aprendizado por dificuldade
    ############################################################################
    # for (style_filename, style_name, style_axis) in styles:
    #     fig = plt.figure(figsize=(10, 8))
    #     fig.suptitle('Histograma de estilo %s' % style_name)
    #     for difficulty in [1, 2, 3, 4, 5]:
    #         mask = (stats['instance'].materials_difficulty == difficulty)
    #
    #         plt.subplot(3, 2, difficulty)
    #         plt.ylabel('Dificuldade %d' % difficulty)
    #         plt.ylim((0, 0.6))
    #         plt.hist(style_axis[mask], bins=11, range=(-5, 6), density=True, rwidth=0.9)
    #
    #     plt.subplot(3, 2, 6)
    #     plt.ylabel('Geral')
    #     plt.ylim((0, 0.6))
    #     plt.hist(style_axis, bins=11, range=(-5, 6), density=True, rwidth=0.9)
    #     plt.savefig(base_folder + '/style_%s_per_difficulty%s.%s' % (style_filename, suffix, format))
    #     plt.close()
    #     # plt.show()
    ############################################################################
