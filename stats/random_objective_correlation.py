import pickle

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import pandas as pd
import seaborn as sns
from scipy.stats import spearmanr

from process.results import normalized_fitness, normalized_objectives

from pprint import pprint

# https://stackoverflow.com/questions/48139899/correlation-matrix-plot-with-coefficients-on-one-side-scatterplots-on-another
def matrix_plot(data, path, method, colors=None):
    def regplot_color(*args, **kwargs):
        ax = sns.regplot(*args, scatter=False, **kwargs)
        ax.scatter(*args, **kwargs['scatter_kws'])

    def corrdot(*args, **kwargs):
        corr_r = args[0].corr(args[1], method)
        # corr_text = f"{corr_r:2.2f}".replace("0.", ".")
        corr_text = ("%2.2f" % corr_r).replace("0.", ".")
        ax = plt.gca()
        ax.set_axis_off()
        marker_size = abs(corr_r) * 9500 + 500
        ax.scatter([.5], [.5], marker_size, [corr_r], alpha=0.6, cmap="coolwarm",
                   vmin=-1, vmax=1, transform=ax.transAxes)
        font_size = abs(corr_r) * 35 + 10
        ax.annotate(corr_text, [.5, .5,],  xycoords="axes fraction",
                    ha='center', va='center', fontsize=font_size)

    sns.set(style='white', font_scale=1.6)
    df = pd.DataFrame(data)

    g = sns.PairGrid(df, aspect=1.4, diag_sharey=False)

    g.map_lower(regplot_color, lowess=True, ci=False, scatter_kws={'s': 15, 'alpha': '.5', 'c': colors}, line_kws={'color': 'black'})
    g.map_diag(sns.distplot, kde_kws={'color': 'black'})
    g.map_upper(corrdot)
    plt.savefig(path)
    plt.close()
    # plt.show()

if __name__ == "__main__":
    base_folder = 'results/2020-05-20 - Correlação separada/'
    filename = 'results/2020-02-22 - Fitness da população aleatória/random_1000.pickle'
    bases_name = [
        'andre_50',
        'andre_100',
        'andre_150',
        'andre_200',
        'andre_250',
        'andre_300',
        'andre_350',
        'andre_400',
        'andre_450',
        'andre_500',
        'andre_550',
        'andre_600',
        'andre_650',
        'andre_700',
        'andre_750',
        'andre_800',
        'andre_850',
        'andre_900',
        'andre_950',
        'andre_1000',
        'real',
    ]

    # (instance, student, individual, function)
    with open(filename, 'rb') as file:
        results = pickle.load(file)

    for i in range(results.shape[0]):
        print('Reading %s' % bases_name[i])

        # (student, individual, function)
        base_result = results[i]
        base_result = base_result[:, :100, :]

        # (student * individual, function)
        all_fitness = base_result.reshape(base_result.shape[0] * base_result.shape[1], base_result.shape[2])

        # print('pearson')
        # matrix_plot(all_fitness, base_folder + '/pearson/correlation_%s.%s' % (bases_name[i], "png"), 'pearson')
        # print('spearman')
        # matrix_plot(all_fitness, base_folder + '/spearman/correlation_%s.%s' % (bases_name[i], "png"), 'spearman')

    limit_size = 100
    results = normalized_objectives('results/2020-02-22 - Fitness da população aleatória/random_1000.pickle', limit_size=limit_size)
    num_instances = results.shape[0]
    num_learners = results.shape[1]

    colors = np.empty((num_instances, num_learners, limit_size), dtype=object)
    colors.fill((0.2980392156862745, 0.4470588235294118, 0.6901960784313725))
    # for i in range(num_instances):
    #     for j in range(num_learners):
    #         colors[i, j, :].fill((i / num_instances, j / num_learners, 0.5))
    colors = colors.flatten()

    type = 1
    if type == 0:
        order_fitness = np.argsort(results, axis=2)
        rank_fitness = np.argsort(order_fitness, axis=2)

        results = results.reshape(results.shape[0] * results.shape[1] * results.shape[2], results.shape[3])
        order_fitness = order_fitness.reshape(order_fitness.shape[0] * order_fitness.shape[1] * order_fitness.shape[2], order_fitness.shape[3])
        rank_fitness = rank_fitness.reshape(rank_fitness.shape[0] * rank_fitness.shape[1] * rank_fitness.shape[2], rank_fitness.shape[3])

        print('Reading %s' % 'total')
        print('pearson')
        matrix_plot(rank_fitness, base_folder + '/pearson_correlation_%s.%s' % ("partial", "png"), 'pearson', colors)
        print('spearman')
        matrix_plot(rank_fitness, base_folder + '/spearman_correlation_%s.%s' % ("partial", "png"), 'spearman', colors)
    elif type == 1:
        results = results.reshape(results.shape[0] * results.shape[1] * results.shape[2], results.shape[3])

        order_fitness = np.argsort(results, axis=0)
        rank_fitness = np.argsort(order_fitness, axis=0)

        print('Reading %s' % 'total')
        print('pearson')
        matrix_plot(rank_fitness, base_folder + '/pearson_correlation_%s.%s' % ("total", "png"), 'pearson', colors)
        print('spearman')
        matrix_plot(rank_fitness, base_folder + '/spearman_correlation_%s.%s' % ("total", "png"), 'spearman', colors)
    elif type == 2:
        order_fitness = np.argsort(results, axis=2)
        rank_fitness = np.argsort(order_fitness, axis=2)

        print('Reading %s' % 'total')
        for i in range(num_instances):
            instance_results = results[i, 0, :, :]

            order_fitness = np.argsort(instance_results, axis=0)
            rank_fitness = np.argsort(order_fitness, axis=0)

            print('pearson')
            matrix_plot(rank_fitness, base_folder + '/pearson_correlation_%d.%s' % (i, "png"), 'pearson')
            print('spearman')
            matrix_plot(rank_fitness, base_folder + '/spearman_correlation_%d.%s' % (i, "png"), 'spearman')

    # (instance * student * individual, function)
    # results = results.reshape(results.shape[0] * results.shape[1] * results.shape[2], results.shape[3])
    # order_fitness = order_fitness.reshape(order_fitness.shape[0] * order_fitness.shape[1] * order_fitness.shape[2], order_fitness.shape[3])
    # rank_fitness = rank_fitness.reshape(rank_fitness.shape[0] * rank_fitness.shape[1] * rank_fitness.shape[2], rank_fitness.shape[3])

    # order_fitness = np.argsort(results, axis=0)
    # rank_fitness = np.argsort(order_fitness, axis=0)
