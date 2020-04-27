import pickle

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import spearmanr


# https://stackoverflow.com/questions/48139899/correlation-matrix-plot-with-coefficients-on-one-side-scatterplots-on-another
def matrix_plot(data, path, method):
    def corrdot(*args, **kwargs):
        corr_r = args[0].corr(args[1], method)
        # corr_text = f"{corr_r:2.2f}".replace("0.", ".")
        corr_text = ("%2.2f" % corr_r).replace("0.", ".")
        ax = plt.gca()
        ax.set_axis_off()
        marker_size = abs(corr_r) * 10000
        ax.scatter([.5], [.5], marker_size, [corr_r], alpha=0.6, cmap="coolwarm",
                   vmin=-1, vmax=1, transform=ax.transAxes)
        font_size = abs(corr_r) * 40 + 5
        ax.annotate(corr_text, [.5, .5,],  xycoords="axes fraction",
                    ha='center', va='center', fontsize=font_size)

    sns.set(style='white', font_scale=1.6)
    df = pd.DataFrame(data)
    g = sns.PairGrid(df, aspect=1.4, diag_sharey=False)
    g.map_lower(sns.regplot, lowess=True, ci=False, line_kws={'color': 'black'})
    g.map_diag(sns.distplot, kde_kws={'color': 'black'})
    g.map_upper(corrdot)
    plt.savefig(path)
    plt.close()
    # plt.show()

if __name__ == "__main__":
    base_folder = 'results/2020-02-22 - Matriz de correlação da população aleatória/'
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

    # Remove 'andre_50'
    results = results[1:, :, :100, :]

    # (instance, student, individual, function)
    total_base_result = results[:, :, :100, :]

    # (instance, student, individual)
    total_sum_result = np.sum(total_base_result, axis=3)

    # (instance, student, 0, 0)
    min_sum_result = np.min(total_sum_result, axis=2)[:, :, np.newaxis, np.newaxis]

    # (instance, student, individual, function)
    normalized_base_result = total_base_result / min_sum_result

    # (instance * student * individual, function)
    total_all_fitness = total_base_result.reshape(total_base_result.shape[0] * total_base_result.shape[1] * total_base_result.shape[2], total_base_result.shape[3])

    # (instance * student * individual, function)
    normalized_all_fitness = normalized_base_result.reshape(total_base_result.shape[0] * total_base_result.shape[1] * total_base_result.shape[2], total_base_result.shape[3])

    print('Reading %s' % 'total')
    print('pearson')
    matrix_plot(normalized_all_fitness, base_folder + '/pearson/correlation_%s.%s' % ("total", "png"), 'pearson')
    print('spearman')
    matrix_plot(normalized_all_fitness, base_folder + '/spearman/correlation_%s.%s' % ("total", "png"), 'spearman')
