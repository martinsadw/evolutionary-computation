import pickle

import numpy as np

if __name__ == "__main__":
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
        # '2020-01-16_andre_550_5_100000.pickle',
        # '2020-01-16_andre_600_5_100000.pickle',
        # '2020-01-16_andre_650_5_100000.pickle',
        # '2020-01-16_andre_700_5_100000.pickle',
        # '2020-01-16_andre_750_5_100000.pickle',
        # '2020-01-16_andre_800_5_100000.pickle',
        # '2020-01-16_andre_850_5_100000.pickle',
        # '2020-01-16_andre_900_5_100000.pickle',
        # '2020-01-16_andre_950_5_100000.pickle',
        # '2020-01-16_andre_1000_5_100000.pickle',
    ]

    for (i, filename) in enumerate(filenames):
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
        all_fitness = np.hstack((all_fitness_ppa_b, all_fitness_ppa_c, all_fitness_pso, all_fitness_ga, all_fitness_de)).T

        print(np.corrcoef(all_fitness_de.T))
