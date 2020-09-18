import datetime
import os
import pickle
import sys

from read.algorithm import create_results_name_list
from process.extremes import get_instances_extremes


# Calculates the worst point and the pareto front for each problem using the
# provided results


instances = ['andre_50', 'andre_300', 'andre_1000', 'real']
algorithms_single = ['ga']
algorithms_multi = ['nsga_ii']
num_objectives_list = [2, 3]

results_name_list = create_results_name_list(instances, algorithms_single, algorithms_multi, num_objectives_list)
extremes_dict = get_instances_extremes(results_name_list)

extremes_path = 'results/extremes'
for ((instance_name, num_objectives), extremes) in extremes_dict.items():
    extremes_file = os.path.join(extremes_path, "%s_%d.pickle" % (instance_name, num_objectives))
    results = {
        'info': {
            'command': os.path.basename(sys.argv[0]) + " " + " ".join(sys.argv[1:]),
            'datetime': str(datetime.datetime.now()),
            'extremes_path': extremes_path,
            'extremes_file': extremes_file,
            'results_name_list': results_name_list,
            'instance_name': instance_name,
            'num_objectives': num_objectives,
            'data_description': '{worst_point: students[(objectives)], nondominated_population: students[(individual, objectives)]}',
        },
        'data': extremes,
    }

    with open(extremes_file, 'wb') as file:
        pickle.dump(results, file)