from read.algorithm import create_results_name_list
from process.extremes import get_instances_extremes


instances = ['andre_50', 'andre_300', 'andre_1000', 'real']
algorithms_single = ['ga']
algorithms_multi = ['nsga_ii']
num_objectives_list = [2, 3]

results_name_list = create_results_name_list(instances, algorithms_single, algorithms_multi, num_objectives_list)
print(results_name_list)
(worst_point, nondominated_population) = get_instances_extremes(results_name_list)

print('Worst point:', worst_point)
print('Nondominated population:', nondominated_population)
