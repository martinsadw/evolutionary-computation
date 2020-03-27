import sys
import pickle

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

font = {'size': 14}
mpl.rc('font', **font)

# http://olsgaard.dk/monochrome-black-white-plots-in-matplotlib.html
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

# color='#4daf4a'
# color='#f781bf'
# color='#a65628'
# color='#377eb8'
# color='#ff7f00'

if __name__ == "__main__":
    savefolder = 'results/2020-01-24 - Gráficos artigo/'
    folder = 'results/2020-01-16 - Resultados base sintética/'
    filenames = [
        '2020-01-16_andre_50_5_100000.pickle',
        '2020-01-16_andre_100_5_100000.pickle',
        '2020-01-16_andre_150_5_100000.pickle',
        '2020-01-16_andre_200_5_100000.pickle',
        '2020-01-16_andre_250_5_100000.pickle',
        '2020-01-16_andre_300_5_100000.pickle',
        '2020-01-16_andre_350_5_100000.pickle',
        '2020-01-16_andre_400_5_100000.pickle',
        '2020-01-16_andre_450_5_100000.pickle',
        '2020-01-16_andre_500_5_100000.pickle',
        '2020-01-16_andre_550_5_100000.pickle',
        '2020-01-16_andre_600_5_100000.pickle',
        '2020-01-16_andre_650_5_100000.pickle',
        '2020-01-16_andre_700_5_100000.pickle',
        '2020-01-16_andre_750_5_100000.pickle',
        '2020-01-16_andre_800_5_100000.pickle',
        '2020-01-16_andre_850_5_100000.pickle',
        '2020-01-16_andre_900_5_100000.pickle',
        '2020-01-16_andre_950_5_100000.pickle',
        '2020-01-16_andre_1000_5_100000.pickle',
    ]
    sizes = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
    quant_instances = len(filenames)

    iteration_fitness = [None] * 5
    cost_values = [None] * 5
    best_fitness = np.empty((5, quant_instances))
    all_best_fitness = np.empty((5, 5 * 24, quant_instances))
    normalization_factors = np.empty((24, quant_instances))

    # for i in range(student_mean_ga.shape[0]):
    #     factor[i] = min(np.min(student_mean_ppa_d[i]),
    #                     np.min(student_mean_ppa_c[i]),
    #                     np.min(student_mean_pso[i]),
    #                     np.min(student_mean_ga[i]),
    #                     np.min(student_mean_de[i])
    #                     )

    # with open(folder + filenames[-1], 'rb') as file:
    #     results = pickle.load(file)
    #
    # cost_de = results['de'][1]
    # results_de = results['de'][2]
    # sum_de = np.sum(results_de, axis=3)
    # mean_de = np.mean(sum_de, axis=0)
    # deviation_de = np.std(sum_de, axis=0)
    #
    # colors = [
    #     '#7e1e9c',
    #     '#15b01a',
    #     '#0343df',
    #     '#ff81c0',
    #     '#653700',
    #     '#e50000',
    #     '#95d0fc',
    #     '#029386',
    #     '#f97306',
    #     '#96f97b',
    #     '#c20078',
    #     '#ffff14',
    #     '#75bbfd',
    #     '#929591',
    #     '#89fe05',
    #     '#bf77f6',
    #     '#9a0eea',
    #     '#033500',
    #     '#06c2ac',
    #     '#c79fef',
    #     '#00035b',
    #     '#d1b26f',
    #     '#00ffff',
    #     '#13eac9',
    # ]
    #
    # for a in range(24):
    #     plt.xlabel('# materials')
    #     plt.ylabel('f(x)')
    #     plt.ylim((0, 30))
    #     plt.plot(cost_de, mean_de[a, :], label=str(a))
    #     plt.fill_between(cost_de, mean_de[a, :] + deviation_de[a, :], mean_de[a, :] - deviation_de[a, :], alpha=0.2)
    #     # plt.legend(loc=2)
    #     # plt.savefig('results/real_test_all%s.%s' % (suffix, format))
    #     # plt.close()
    #     plt.show()
    #
    # assert(False)

    for (i, filename) in enumerate(filenames):
        with open(folder + filename, 'rb') as file:
            results = pickle.load(file)

        if iteration_fitness[0] is None:
            # (iteration, instance)
            iteration_fitness[0] = np.zeros((results['ppa_d'][2].shape[2],))
            iteration_fitness[1] = np.zeros((results['ppa_c'][2].shape[2],))
            iteration_fitness[2] = np.zeros((results['pso'][2].shape[2],))
            iteration_fitness[3] = np.zeros((results['ga'][2].shape[2],))
            iteration_fitness[4] = np.zeros((results['de'][2].shape[2],))

            cost_values[0] = results['ppa_d'][1]
            cost_values[1] = results['ppa_c'][1]
            cost_values[2] = results['pso'][1]
            cost_values[3] = results['ga'][1]
            cost_values[4] = results['de'][1]

        print('Reading %s' % filename)

        # (execution, student, iteration, function)
        results_ppa_d = results['ppa_d'][2]
        results_ppa_c = results['ppa_c'][2]
        results_pso = results['pso'][2]
        results_ga = results['ga'][2]
        results_de = results['de'][2]

        # (execution, student, iteration)
        # Fitness total
        # # O somatório é realizado pois o problema é definido como a soma das funções objetivos
        iteration_fitness_ppa_d = np.sum(results_ppa_d, axis=3)
        iteration_fitness_ppa_c = np.sum(results_ppa_c, axis=3)
        iteration_fitness_pso = np.sum(results_pso, axis=3)
        iteration_fitness_ga = np.sum(results_ga, axis=3)
        iteration_fitness_de = np.sum(results_de, axis=3)

        # (execution, student)
        # Melhor fitness total
        # # Apenas o resultado final é utilizado no calculo do fator de normalização
        fitness_ppa_d = iteration_fitness_ppa_d[:, :, -1]
        fitness_ppa_c = iteration_fitness_ppa_c[:, :, -1]
        fitness_pso = iteration_fitness_pso[:, :, -1]
        fitness_ga = iteration_fitness_ga[:, :, -1]
        fitness_de = iteration_fitness_de[:, :, -1]

        # (student, instance)
        # # Um problema é definido por um par (student, instance).
        # # O fator de normalização é o menor resultado encontrado para um problema
        for j in range(fitness_de.shape[1]):
            normalization_factors[j, i] = min(np.min(fitness_ppa_d[:, j]),
                                              np.min(fitness_ppa_c[:, j]),
                                              np.min(fitness_pso[:, j]),
                                              np.min(fitness_ga[:, j]),
                                              np.min(fitness_de[:, j]))

        # (student, iteration)
        # Fitness total da média de um estudante de uma instância
        # # As multiplas execuções de um problema evitam a aleatoriedade dos algoritmos.
        iteration_mean_ppa_d = np.mean(iteration_fitness_ppa_d, axis=0)
        iteration_mean_ppa_c = np.mean(iteration_fitness_ppa_c, axis=0)
        iteration_mean_pso = np.mean(iteration_fitness_pso, axis=0)
        iteration_mean_ga = np.mean(iteration_fitness_ga, axis=0)
        iteration_mean_de = np.mean(iteration_fitness_de, axis=0)

        # (iteration)
        # Fitness total da média de todos os resutados de uma instância
        # # O fitness normalizado serve para remover as variações de intervalo de valor entre problemas diferentes
        normalized_mean_ppa_d = np.mean(iteration_mean_ppa_d / normalization_factors[:, i][:, np.newaxis], axis=0)
        normalized_mean_ppa_c = np.mean(iteration_mean_ppa_c / normalization_factors[:, i][:, np.newaxis], axis=0)
        normalized_mean_pso = np.mean(iteration_mean_pso / normalization_factors[:, i][:, np.newaxis], axis=0)
        normalized_mean_ga = np.mean(iteration_mean_ga / normalization_factors[:, i][:, np.newaxis], axis=0)
        normalized_mean_de = np.mean(iteration_mean_de / normalization_factors[:, i][:, np.newaxis], axis=0)

        best_fitness[0, i] = normalized_mean_ppa_d[-1]
        best_fitness[1, i] = normalized_mean_ppa_c[-1]
        best_fitness[2, i] = normalized_mean_pso[-1]
        best_fitness[3, i] = normalized_mean_ga[-1]
        best_fitness[4, i] = normalized_mean_de[-1]

        iteration_fitness[0] += normalized_mean_ppa_d
        iteration_fitness[1] += normalized_mean_ppa_c
        iteration_fitness[2] += normalized_mean_pso
        iteration_fitness[3] += normalized_mean_ga
        iteration_fitness[4] += normalized_mean_de

        # (execution * student)
        normalized_fitness_ppa_d = (fitness_ppa_d / normalization_factors[:, i]).ravel()
        normalized_fitness_ppa_c = (fitness_ppa_c / normalization_factors[:, i]).ravel()
        normalized_fitness_pso = (fitness_pso / normalization_factors[:, i]).ravel()
        normalized_fitness_ga = (fitness_ga / normalization_factors[:, i]).ravel()
        normalized_fitness_de = (fitness_de / normalization_factors[:, i]).ravel()

        all_best_fitness[0, :, i] = normalized_fitness_ppa_d
        all_best_fitness[1, :, i] = normalized_fitness_ppa_c
        all_best_fitness[2, :, i] = normalized_fitness_pso
        all_best_fitness[3, :, i] = normalized_fitness_ga
        all_best_fitness[4, :, i] = normalized_fitness_de

    # iteration_fitness[0] /= quant_instances
    # iteration_fitness[1] /= quant_instances
    # iteration_fitness[2] /= quant_instances
    # iteration_fitness[3] /= quant_instances
    # iteration_fitness[4] /= quant_instances

    ############################################################################

    functions_fitness_andre_700 = None
    functions_fitness_andre_300 = None
    functions_fitness_andre_50 = None
    functions_fitness_real = None
    cost_andre_700 = None
    cost_andre_300 = None
    cost_andre_50 = None
    cost_real = None

    with open(folder + '2020-01-16_andre_700_5_100000.pickle', 'rb') as file:
        results = pickle.load(file)
        # (execution, student, iteration, function)
        results_de = results['de'][2]
        # (iteration, function)
        iteration_mean_de = np.mean(results_de, axis=(0, 1))
        functions_fitness_andre_700 = iteration_mean_de
        cost_andre_700 = results['de'][1]

    with open(folder + '2020-01-16_andre_300_5_100000.pickle', 'rb') as file:
        results = pickle.load(file)
        # (execution, student, iteration, function)
        results_de = results['de'][2]
        # (iteration, function)
        iteration_mean_de = np.mean(results_de, axis=(0, 1))
        functions_fitness_andre_300 = iteration_mean_de
        cost_andre_300 = results['de'][1]

    with open(folder + '2020-01-16_andre_50_5_100000.pickle', 'rb') as file:
        results = pickle.load(file)
        # (execution, student, iteration, function)
        results_de = results['de'][2]
        # (iteration, function)
        iteration_mean_de = np.mean(results_de, axis=(0, 1))
        functions_fitness_andre_50 = iteration_mean_de
        cost_andre_50 = results['de'][1]

    with open(folder + '2020-01-16_real_5_100000.pickle', 'rb') as file:
        results = pickle.load(file)
        # (execution, student, iteration, function)
        results_de = results['de'][2]
        # (iteration, function)
        iteration_mean_de = np.mean(results_de, axis=(0, 1))
        functions_fitness_real = iteration_mean_de
        cost_real = results['de'][1]

    ############################################################################

    plt.xlabel('# materials')
    plt.ylabel('normalized f(x)')
    plt.boxplot(all_best_fitness[1], medianprops=dict(color=color[0]))
    plt.xticks(range(1, quant_instances + 1), sizes)
    plt.savefig(savefolder + 'alt_boxplot_ppa_c_instances%s.%s' % (suffix, format))
    plt.close()

    for (i, method) in enumerate(['ppa', 'ppa_c', 'pso', 'ga', 'de']):
        plt.xlabel('# materials')
        plt.ylabel('normalized f(x)')
        plt.ylim((0, 21))
        plt.boxplot(all_best_fitness[i], medianprops=dict(color=color[0]))
        plt.xticks(np.arange(quant_instances)[1::2] + 1, sizes[1::2])
        plt.savefig(savefolder + ('boxplot_%s_instances%s.%s' % (method, suffix, format)))
        plt.close()
        # plt.show()

    plt.figure(figsize=(12.8, 4.8))
    fig, ax = plt.subplots()
    ax.set_prop_cycle(graphics_cycler)
    plt.xlabel('# materials')
    plt.ylabel('normalized f(x)')
    plt.plot(sizes, best_fitness[0], label="PPA")
    # plt.plot(sizes, best_fitness[1], label="PPAC")
    plt.plot(sizes, best_fitness[2], label="PSO")
    plt.plot(sizes, best_fitness[3], label="GA")
    plt.plot(sizes, best_fitness[4], label="DE")
    plt.xticks(sizes[1::2])
    plt.legend(loc=2)
    plt.savefig(savefolder + 'instances_comparison%s.%s' % (suffix, format))
    plt.close()
    # plt.show()

    plt.figure(figsize=(12.8, 4.8))
    fig, ax = plt.subplots()
    ax.set_prop_cycle(graphics_cycler)
    plt.xlabel('# materials')
    plt.ylabel('normalized f(x)')
    plt.ylim((0, 5))
    plt.plot(sizes, best_fitness[0], label="PPA")
    # plt.plot(sizes, best_fitness[1], label="PPAC")
    plt.plot(sizes, best_fitness[2], label="PSO")
    plt.plot(sizes, best_fitness[3], label="GA")
    plt.plot(sizes, best_fitness[4], label="DE")
    plt.xticks(sizes[1::2])
    plt.legend(loc=2)
    plt.savefig(savefolder + 'instances_comparison_zoom%s.%s' % (suffix, format))
    plt.close()
    # plt.show()

    fig, ax = plt.subplots()
    ax.set_prop_cycle(graphics_cycler)
    plt.xlabel('# objective function evaluation')
    plt.ylabel('normalized f(x)')
    plt.plot(cost_values[0], iteration_fitness[0], markevery=300, label="PPA")
    # plt.plot(cost_values[1], iteration_fitness[1], markevery=300, label="PPAC")
    plt.plot(cost_values[2], iteration_fitness[2], markevery=300, label="PSO")
    plt.plot(cost_values[3], iteration_fitness[3], markevery=300, label="GA")
    plt.plot(cost_values[4], iteration_fitness[4], markevery=300, label="DE")
    plt.legend(loc=1)
    # plt.savefig(savefolder + 'convergence_comparison%s.%s' % (suffix, format))
    # plt.close()
    plt.show()

    fig, ax = plt.subplots()
    ax.set_prop_cycle(graphics_cycler)
    plt.xlabel('# objective function evaluation')
    plt.ylabel('normalized f(x)')
    plt.ylim((1, 9))
    plt.plot(cost_values[0], iteration_fitness[0], markevery=300, label="PPA")
    # plt.plot(cost_values[1], iteration_fitness[1], markevery=300, label="PPAC")
    plt.plot(cost_values[2], iteration_fitness[2], markevery=300, label="PSO")
    plt.plot(cost_values[3], iteration_fitness[3], markevery=300, label="GA")
    plt.plot(cost_values[4], iteration_fitness[4], markevery=300, label="DE")
    plt.legend(loc=1)
    plt.savefig(savefolder + 'convergence_comparison_zoom%s.%s' % (suffix, format))
    plt.close()
    # plt.show()

    fig, ax = plt.subplots()
    ax.set_prop_cycle(graphics_cycler)
    plt.xlabel('# objective function evaluation')
    plt.ylabel('objective value')
    plt.ylim((-1, 12))
    plt.plot(cost_andre_700, functions_fitness_andre_700[:, 0], markevery=300, label="O1")
    plt.plot(cost_andre_700, functions_fitness_andre_700[:, 1], markevery=300, label="O2")
    plt.plot(cost_andre_700, functions_fitness_andre_700[:, 2], markevery=300, label="O3")
    plt.plot(cost_andre_700, functions_fitness_andre_700[:, 3], markevery=300, label="O4")
    plt.plot(cost_andre_700, functions_fitness_andre_700[:, 4], markevery=300, label="O5")
    plt.legend(loc=1)
    plt.savefig(savefolder + 'functions_700%s.%s' % (suffix, format))
    plt.close()
    # plt.show()

    fig, ax = plt.subplots()
    ax.set_prop_cycle(graphics_cycler)
    plt.xlabel('# objective function evaluation')
    plt.ylabel('objective value')
    plt.ylim((-1, 12))
    plt.plot(cost_andre_300, functions_fitness_andre_300[:, 0], markevery=300, label="O1")
    plt.plot(cost_andre_300, functions_fitness_andre_300[:, 1], markevery=300, label="O2")
    plt.plot(cost_andre_300, functions_fitness_andre_300[:, 2], markevery=300, label="O3")
    plt.plot(cost_andre_300, functions_fitness_andre_300[:, 3], markevery=300, label="O4")
    plt.plot(cost_andre_300, functions_fitness_andre_300[:, 4], markevery=300, label="O5")
    plt.legend(loc=1)
    plt.savefig(savefolder + 'functions_300%s.%s' % (suffix, format))
    plt.close()
    # plt.show()

    fig, ax = plt.subplots()
    ax.set_prop_cycle(graphics_cycler)
    plt.xlabel('# objective function evaluation')
    plt.ylabel('objective value')
    plt.ylim((-1, 12))
    plt.plot(cost_andre_50, functions_fitness_andre_50[:, 0], markevery=300, label="O1")
    plt.plot(cost_andre_50, functions_fitness_andre_50[:, 1], markevery=300, label="O2")
    plt.plot(cost_andre_50, functions_fitness_andre_50[:, 2], markevery=300, label="O3")
    plt.plot(cost_andre_50, functions_fitness_andre_50[:, 3], markevery=300, label="O4")
    plt.plot(cost_andre_50, functions_fitness_andre_50[:, 4], markevery=300, label="O5")
    plt.legend(loc=1)
    plt.savefig(savefolder + 'functions_50%s.%s' % (suffix, format))
    plt.close()
    # plt.show()

    fig, ax = plt.subplots()
    ax.set_prop_cycle(graphics_cycler)
    plt.xlabel('# objective function evaluation')
    plt.ylabel('objective value')
    plt.ylim((-1, 12))
    plt.plot(cost_real, functions_fitness_real[:, 0], markevery=300, label="O1")
    plt.plot(cost_real, functions_fitness_real[:, 1], markevery=300, label="O2")
    plt.plot(cost_real, functions_fitness_real[:, 2], markevery=300, label="O3")
    plt.plot(cost_real, functions_fitness_real[:, 3], markevery=300, label="O4")
    plt.plot(cost_real, functions_fitness_real[:, 4], markevery=300, label="O5")
    plt.legend(loc=1)
    plt.savefig(savefolder + 'functions_real%s.%s' % (suffix, format))
    plt.close()
    # plt.show()
