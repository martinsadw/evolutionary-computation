import datetime
import os
import pickle
import random
import sys

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import spearmanr

from acs.objective import fitness
from acs.instance import Instance, print_instance

from utils.timer import Timer


if __name__ == "__main__":
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
        ('real', 'real/instance.txt'),
    ]

    population_size = 1000
    seed = 0
    results_name = 'results/random_population/random_%d.pickle' % population_size

    quant_instances = len(filenames)
    data = np.empty((quant_instances, 24, population_size, 5))
    instances = []

    results = {
        'info': {
            'command': os.path.basename(sys.argv[0]) + " " + " ".join(sys.argv[1:]),
            'datetime': str(datetime.datetime.now()),
            'seed': seed,
            'results_name': results_name,
        },
    }

    np.random.seed(seed)
    random.seed(seed)
    for (i, (base, filename)) in enumerate(filenames):
        print('Reading %s' % (folder + filename))

        instance = Instance.load_from_file(folder + filename)
        instances.append(instance)
        timer = Timer()

        for student in range(instance.num_learners):
            print('%d / %d' % (student, instance.num_learners))

            population = np.random.randint(2, size=(population_size, instance.num_materials), dtype=bool)
            survival_values = []
            np.apply_along_axis(fitness, 1, population, instance, student, timer, data=survival_values)
            data[i, student, :, :] = survival_values

    results['info']['instances'] = instances
    results['data'] = data
    print(data)
    print(data.shape)

    with open(results_name, 'wb') as file:
        pickle.dump(results, file)
