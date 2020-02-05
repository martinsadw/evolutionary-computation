import sys
import pickle

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

font = {'size': 14}
mpl.rc('font', **font)

use_grayscale = True
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

if __name__ == "__main__":
    savefolder = 'results/2020-01-24 - Gráficos artigo/'
    folder = 'results/2020-01-16 - Resultados base sintética/'
    filename = '2020-01-16_real_5_100000.pickle'

    with open(folder + filename, 'rb') as file:
        results = pickle.load(file)

    print('Reading %s' % filename)

    # (iteration)
    cost_ppa_b = results['ppa_b'][1]
    cost_ppa_c = results['ppa_c'][1]
    cost_pso = results['pso'][1]
    cost_ga = results['ga'][1]
    cost_de = results['de'][1]

    # (execution, student, iteration, function)
    results_ppa_b = results['ppa_b'][2]
    results_ppa_c = results['ppa_c'][2]
    results_pso = results['pso'][2]
    results_ga = results['ga'][2]
    results_de = results['de'][2]

    # (execution, student, iteration)
    # Fitness total
    # # O somatório é realizado pois o problema é definido como a soma das funções objetivos
    iteration_fitness_ppa_b = np.sum(results_ppa_b, axis=3)
    iteration_fitness_ppa_c = np.sum(results_ppa_c, axis=3)
    iteration_fitness_pso = np.sum(results_pso, axis=3)
    iteration_fitness_ga = np.sum(results_ga, axis=3)
    iteration_fitness_de = np.sum(results_de, axis=3)

    # (execution, student)
    # Melhor fitness total
    # # Apenas o resultado final é utilizado no calculo do fator de normalização
    fitness_ppa_b = iteration_fitness_ppa_b[:, :, -1]
    fitness_ppa_c = iteration_fitness_ppa_c[:, :, -1]
    fitness_pso = iteration_fitness_pso[:, :, -1]
    fitness_ga = iteration_fitness_ga[:, :, -1]
    fitness_de = iteration_fitness_de[:, :, -1]

    # (student, instance)
    # # Um problema é definido por um par (student, instance).
    # # O fator de normalização é o menor resultado encontrado para um problema
    normalization_factors = np.empty((24,))
    for j in range(fitness_de.shape[1]):
        normalization_factors[j] = min(np.min(fitness_ppa_b[:, j]),
                                          np.min(fitness_ppa_c[:, j]),
                                          np.min(fitness_pso[:, j]),
                                          np.min(fitness_ga[:, j]),
                                          np.min(fitness_de[:, j]))

    # (student, iteration)
    # Fitness total da média de um estudante de uma instância
    # # As multiplas execuções de um problema evitam a aleatoriedade dos algoritmos.
    iteration_mean_ppa_b = np.mean(iteration_fitness_ppa_b, axis=0)
    iteration_mean_ppa_c = np.mean(iteration_fitness_ppa_c, axis=0)
    iteration_mean_pso = np.mean(iteration_fitness_pso, axis=0)
    iteration_mean_ga = np.mean(iteration_fitness_ga, axis=0)
    iteration_mean_de = np.mean(iteration_fitness_de, axis=0)

    # (iteration)
    # Fitness total da média de todos os resutados de uma instância
    # # O fitness normalizado serve para remover as variações de intervalo de valor entre problemas diferentes
    normalized_mean_ppa_b = np.mean(iteration_mean_ppa_b / normalization_factors[:, np.newaxis], axis=0)
    normalized_mean_ppa_c = np.mean(iteration_mean_ppa_c / normalization_factors[:, np.newaxis], axis=0)
    normalized_mean_pso = np.mean(iteration_mean_pso / normalization_factors[:, np.newaxis], axis=0)
    normalized_mean_ga = np.mean(iteration_mean_ga / normalization_factors[:, np.newaxis], axis=0)
    normalized_mean_de = np.mean(iteration_mean_de / normalization_factors[:, np.newaxis], axis=0)

    ############################################################################

    fig, ax = plt.subplots()
    ax.set_prop_cycle(graphics_cycler)
    plt.xlabel('# objective function evaluation')
    plt.ylabel('normalized f(x)')
    plt.plot(cost_ppa_b, normalized_mean_ppa_b, markevery=300, label="PPA")
    # plt.plot(cost_ppa_c, normalized_mean_ppa_c, markevery=300, label="PPAC")
    plt.plot(cost_pso, normalized_mean_pso, markevery=300, label="PSO")
    plt.plot(cost_ga, normalized_mean_ga, markevery=300, label="GA")
    plt.plot(cost_de, normalized_mean_de, markevery=300, label="DE")
    plt.legend(loc=1)
    plt.savefig(savefolder + 'convergence_comparison_real%s.%s' % (suffix, format))
    plt.close()
    # plt.show()

    fig, ax = plt.subplots()
    ax.set_prop_cycle(graphics_cycler)
    plt.xlabel('# objective function evaluation')
    plt.ylabel('normalized f(x)')
    plt.ylim((1, 3))
    plt.plot(cost_ppa_b, normalized_mean_ppa_b, markevery=300, label="PPA")
    # plt.plot(cost_ppa_c, normalized_mean_ppa_c, markevery=300, label="PPAC")
    plt.plot(cost_pso, normalized_mean_pso, markevery=300, label="PSO")
    plt.plot(cost_ga, normalized_mean_ga, markevery=300, label="GA")
    plt.plot(cost_de, normalized_mean_de, markevery=300, label="DE")
    plt.legend(loc=1)
    plt.savefig(savefolder + 'convergence_comparison_zoom_real%s.%s' % (suffix, format))
    plt.close()
    # plt.show()
