import math
import pickle

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, pearsonr, binned_statistic_2d, t


def trim_zeros_2D(array, axis=1):
    mask = ~(array==0).all(axis=axis)
    inv_mask = mask[::-1]
    start_idx = np.argmax(mask == True)
    end_idx = len(inv_mask) - np.argmax(inv_mask == True)
    if axis:
        return array[start_idx:end_idx,:]
    else:
        return array[:, start_idx:end_idx]

def plot_corr(data):
    fig = plt.figure(figsize=(9, 9))
    for j in range(5):
        for i in range(j):
            ax = plt.subplot(4, 4, i + (j - 1) * 4 + 1)
            # plt.hist2d(data[i], data[j], bins=100, cmin=50)
            histogram = binned_statistic_2d(data[i], data[j], data[i], 'count', bins=200).statistic
            histogram[histogram < 10] = 0
            histogram = trim_zeros_2D(histogram, 0)
            histogram = trim_zeros_2D(histogram, 1)
            im = ax.imshow(histogram, origin='lower', vmin=0)

    plt.show()


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

    # Remove 'andre_50'
    results = results[1:, :, :, :]

    # (instance, student, individual, function)
    total_base_result = results[:, :, :1, :]


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

    normalized_all_fitness = normalized_all_fitness.T

    print(normalized_all_fitness.shape)

    # plot_corr(normalized_all_fitness)

    print('Pearson')
    for j in range(5):
        for i in range(5):
            print('%.20f' % pearsonr(normalized_all_fitness[i], normalized_all_fitness[j])[1], end=' ')
        print('')

    print('Self Pearson')
    for j in range(5):
        for i in range(5):
            corr = pearsonr(normalized_all_fitness[i], normalized_all_fitness[j])[0]
            print('%f * sqrt((%d - 2) / (1 - %f))' % (corr, normalized_all_fitness.shape[1], corr ** 2), end=' ')
            # print('%.3f' % (corr * math.sqrt((normalized_all_fitness.shape[1] - 2) / (1 - (corr ** 2)))), end=' ')
        print('')

    print('Self Pearson')
    for j in range(5):
        for i in range(5):
            corr = pearsonr(normalized_all_fitness[i], normalized_all_fitness[j])[0]
            # print('%f * sqrt((%d - 2) / (1 - %f))' % (corr, normalized_all_fitness.shape[1], corr ** 2), end=' ')
            print('%15.3f' % (corr * math.sqrt((normalized_all_fitness.shape[1] - 2) / (1 - (corr ** 2)))), end=' ')
        print('')

    print('Spearman')
    for j in range(5):
        for i in range(5):
            print('%.20f' % spearmanr(normalized_all_fitness[i], normalized_all_fitness[j]).pvalue, end=' ')
        print('')

    print('Self Spearman')
    for j in range(5):
        for i in range(5):
            corr = spearmanr(normalized_all_fitness[i], normalized_all_fitness[j]).correlation
            print('%.3f' % (corr * math.sqrt((normalized_all_fitness.shape[1] - 2) / (1 - (corr ** 2)))), end=' ')
        print('')

    print(t.cdf(0.975, 60) * 2)
