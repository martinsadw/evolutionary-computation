import sys

import numpy as np
import matplotlib.pyplot as plt

from ppa.ppa import prey_predator_algorithm
from ppa.config import Config
from acs.objective import fitness, fitness_population
from acs.instance import Instance, print_instance

def read_files(instance_config_filename, config_filename):
    if instance_config_filename is None:
        instance = Instance.load_test()
    else:
        instance = Instance.load_from_file(instance_config_filename)

    # print_instance(instance)
    # print("")

    if config_filename is None:
        config = Config.load_test()
    else:
        config = Config.load_from_file(config_filename)

    return (instance, config)


# assert(len(sys.argv) >= 2)
instance_config_filename = None
if (len(sys.argv) >= 2):
    instance_config_filename = sys.argv[1]

config_filename = None
if (len(sys.argv) >= 3):
    config_filename = sys.argv[2]

num_repetitions = 10

(instance, config) = read_files(instance_config_filename, config_filename)
best_fitness = np.zeros((config.num_iterations + 1, num_repetitions)) # Um valor extra para salvar os valores iniciais
perf_counter = np.zeros((config.num_iterations + 1, num_repetitions))
process_time = np.zeros((config.num_iterations + 1, num_repetitions))

for i in range(num_repetitions):
    (population, survival_values) = prey_predator_algorithm(instance, config, fitness_population, best_fitness=best_fitness[:,i], perf_counter=perf_counter[:,i], process_time=process_time[:,i])
    print('#{}\n'.format(i))
    print('Survival values:\n{}\n'.format(survival_values))
    print('Best Individual:\n{}\n'.format(population[0]))

mean_best_fitness = np.mean(best_fitness, axis=1)
mean_perf_counter = np.mean(perf_counter, axis=1)
mean_process_time = np.mean(process_time, axis=1)

print('Statistics:')
print('Fitness:\n{}\n'.format(mean_best_fitness))
print('perf_counter:\n{}\n'.format(mean_perf_counter))
print('process_time:\n{}\n'.format(mean_process_time))

fig = plt.figure()
fig.suptitle('PPA: perf_counter vs. process_time')
plt.plot(mean_perf_counter, 'r.')
plt.plot(mean_process_time, 'b.')
plt.show()

fig = plt.figure()
fig.suptitle('PPA: best fitness')
plt.plot(mean_best_fitness, 'r')
plt.show()
