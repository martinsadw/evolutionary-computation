import pickle

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import spearmanr

from acs.objective import fitness
from acs.instance import Instance, print_instance

from utils.timer import Timer


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
    save_folder = 'results/2020-02-22 - Fitness da população aleatória/'
    save_filename = 'random_%d.pickle'
    folder = 'instances/'
    filenames = [
        ('andre_50', 'andre/50/instance.txt'),
        ('andre_100', 'andre/100/instance.txt'),
        ('andre_150', 'andre/150/instance.txt'),
        ('andre_200', 'andre/200/instance.txt'),
        ('andre_250', 'andre/250/instance.txt'),
        ('andre_300', 'andre/300/instance.txt'),
        ('andre_350', 'andre/350/instance.txt'),
        ('andre_400', 'andre/400/instance.txt'),
        ('andre_450', 'andre/450/instance.txt'),
        ('andre_500', 'andre/500/instance.txt'),
        ('andre_550', 'andre/550/instance.txt'),
        ('andre_600', 'andre/600/instance.txt'),
        ('andre_650', 'andre/650/instance.txt'),
        ('andre_700', 'andre/700/instance.txt'),
        ('andre_750', 'andre/750/instance.txt'),
        ('andre_800', 'andre/800/instance.txt'),
        ('andre_850', 'andre/850/instance.txt'),
        ('andre_900', 'andre/900/instance.txt'),
        ('andre_950', 'andre/950/instance.txt'),
        ('andre_1000', 'andre/1000/instance.txt'),
        ('real', 'real/test_instance.txt'),
    ]

    population_size = 1000

    quant_instances = len(filenames)
    results = np.empty((quant_instances, 24, population_size, 5))

    np.random.seed(0)
    for (i, (base, filename)) in enumerate(filenames):
        print('Reading %s' % (folder + filename))

        instance = Instance.load_from_file(folder + filename)
        timer = Timer()

        for student in range(instance.num_learners):
            print('%d / %d' % (student, instance.num_learners))

            population = np.random.randint(2, size=(population_size, instance.num_materials), dtype=bool)
            survival_values = []
            np.apply_along_axis(fitness, 1, population, instance, student, timer, data=survival_values)
            results[i, student, :, :] = survival_values

    print(results)
    print(results.shape)

    with open(save_folder + (save_filename % population_size), 'wb') as file:
        pickle.dump(results, file)
