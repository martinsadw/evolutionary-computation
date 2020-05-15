import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd

from process.results import normalized_fitness, normalized_objectives

data = normalized_fitness('results/2020-02-22 - Fitness da população aleatória/random_1000.pickle', limit_size=100)
data2 = normalized_objectives('results/2020-02-22 - Fitness da população aleatória/random_1000.pickle', limit_size=100)

print(data)
print(data2)
print(np.min(data, axis=0))
print(np.min(data2, axis=0))

# for i in range(5):
#     my_data = pd.Series(data[:, i])
#     my_data.plot(kind = 'box')
#
#     sm.qqplot(data[:, i], fit=True, line='45')
#     plt.show()
