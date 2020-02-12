import pickle

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import spearmanr


# https://stackoverflow.com/questions/48139899/correlation-matrix-plot-with-coefficients-on-one-side-scatterplots-on-another
def matrix_plot(data, path):
    def corrdot(*args, **kwargs):
        corr_r = args[0].corr(args[1], 'spearman')
        corr_text = f"{corr_r:2.2f}".replace("0.", ".")
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
    base_folder = 'results/2020-02-12 - Matriz de correlação spearman/'
    folder = 'results/2020-01-16 - Resultados base sintética/'
    filenames = [
        ('andre_50', '2020-01-16_andre_50_5_100000.pickle'),
        ('andre_100', '2020-01-16_andre_100_5_100000.pickle'),
        ('andre_150', '2020-01-16_andre_150_5_100000.pickle'),
        ('andre_200', '2020-01-16_andre_200_5_100000.pickle'),
        ('andre_250', '2020-01-16_andre_250_5_100000.pickle'),
        ('andre_300', '2020-01-16_andre_300_5_100000.pickle'),
        ('andre_350', '2020-01-16_andre_350_5_100000.pickle'),
        ('andre_400', '2020-01-16_andre_400_5_100000.pickle'),
        ('andre_450', '2020-01-16_andre_450_5_100000.pickle'),
        ('andre_500', '2020-01-16_andre_500_5_100000.pickle'),
        ('andre_550', '2020-01-16_andre_550_5_100000.pickle'),
        ('andre_600', '2020-01-16_andre_600_5_100000.pickle'),
        ('andre_650', '2020-01-16_andre_650_5_100000.pickle'),
        ('andre_700', '2020-01-16_andre_700_5_100000.pickle'),
        ('andre_750', '2020-01-16_andre_750_5_100000.pickle'),
        ('andre_800', '2020-01-16_andre_800_5_100000.pickle'),
        ('andre_850', '2020-01-16_andre_850_5_100000.pickle'),
        ('andre_900', '2020-01-16_andre_900_5_100000.pickle'),
        ('andre_950', '2020-01-16_andre_950_5_100000.pickle'),
        ('andre_1000', '2020-01-16_andre_1000_5_100000.pickle'),
        ('real', '2020-01-16_real_5_100000.pickle'),
    ]

    total_all_fitness = np.empty((5, 0))

    for (i, (base, filename)) in enumerate(filenames):
        with open(folder + filename, 'rb') as file:
            results = pickle.load(file)

        print('Reading %s' % filename)

        # (execution, student, iteration, function)
        results_ppa_b = results['ppa_b'][2]
        results_ppa_c = results['ppa_c'][2]
        results_pso = results['pso'][2]
        results_ga = results['ga'][2]
        results_de = results['de'][2]

        # (execution, student, function)
        fitness_ppa_b = results_ppa_b[:, :, -1, :]
        fitness_ppa_c = results_ppa_c[:, :, -1, :]
        fitness_pso = results_pso[:, :, -1, :]
        fitness_ga = results_ga[:, :, -1, :]
        fitness_de = results_de[:, :, -1, :]

        # (execution * student, function)
        all_fitness_ppa_b = fitness_ppa_b.reshape(fitness_ppa_b.shape[0] * fitness_ppa_b.shape[1], fitness_ppa_b.shape[2])
        all_fitness_ppa_c = fitness_ppa_c.reshape(fitness_ppa_c.shape[0] * fitness_ppa_c.shape[1], fitness_ppa_c.shape[2])
        all_fitness_pso = fitness_pso.reshape(fitness_pso.shape[0] * fitness_pso.shape[1], fitness_pso.shape[2])
        all_fitness_ga = fitness_ga.reshape(fitness_ga.shape[0] * fitness_ga.shape[1], fitness_ga.shape[2])
        all_fitness_de = fitness_de.reshape(fitness_de.shape[0] * fitness_de.shape[1], fitness_de.shape[2])

        # (function, execution * student * 5)
        all_fitness = np.vstack((all_fitness_ppa_b, all_fitness_ppa_c, all_fitness_pso, all_fitness_ga, all_fitness_de)).T
        total_all_fitness = np.hstack((total_all_fitness, all_fitness))

        # correlation = np.corrcoef(all_fitness)
        (correlation, p) = spearmanr(all_fitness, axis=1)
        print(correlation)

        matrix_plot(all_fitness.T, base_folder + '/correlation_%s.%s' % (base, "png"))
        # fig, ax = plt.subplots()
        # im = ax.imshow(correlation)
        # fig.colorbar(im, orientation="horizontal", aspect=40)
        # ax.set_xticks(range(5))
        # ax.set_xticklabels(["O1", "O2", "O3", "O4", "O5"])
        # ax.set_yticks(range(5))
        # ax.set_yticklabels(["O1", "O2", "O3", "O4", "O5"])
        # plt.savefig(base_folder + '/correlation_%s.%s' % (base, "png"))
        # plt.close()
        # # plt.show()

    # total_correlation = np.corrcoef(total_all_fitness)
    (total_correlation, total_p) = spearmanr(total_all_fitness, axis=1)
    print(total_correlation)

    # matrix_plot(total_all_fitness.T, base_folder + '/correlation_%s.%s' % ("total", "png"))
    # fig, ax = plt.subplots()
    # im = ax.imshow(total_correlation)
    # fig.colorbar(im, orientation="horizontal", aspect=40)
    # ax.set_xticks(range(5))
    # ax.set_xticklabels(["O1", "O2", "O3", "O4", "O5"])
    # ax.set_yticks(range(5))
    # ax.set_yticklabels(["O1", "O2", "O3", "O4", "O5"])
    # plt.savefig(base_folder + '/correlation_%s.%s' % ("total", "png"))
    # plt.close()
    # # plt.show()
