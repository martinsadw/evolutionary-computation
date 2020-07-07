import os

import numpy as np

from process.comparison import read_results


# (instance, student, individual, objective)
data = read_results('results/random_population/random_1000.pickle', limit_size=1000)

num_students = data.shape[1]

results_folder = 'results/2020-07-02 - CSV separado por estudante'
path_real = os.path.join(results_folder, 'real')
path_1000 = os.path.join(results_folder, '1000')
os.makedirs(path_real, exist_ok=True)
os.makedirs(path_1000, exist_ok=True)
for i in range(num_students):
    np.savetxt(os.path.join(path_real, '%02d.csv' % i), data[-1, i, :, :], delimiter=',')
    np.savetxt(os.path.join(path_1000, '%02d.csv' % i), data[-2, i, :, :], delimiter=',')
