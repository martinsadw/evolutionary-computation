import os
import pickle


def create_extremes_name_list(instances, num_objectives_list):
    extremes_name = [(instance, num_objectives) for instance in instances for num_objectives in num_objectives_list]

    return extremes_name

def get_extremes_name(instance, num_objectives):
    name = '%s_%s.pickle' % (instance, num_objectives)
    return name

def open_extremes(name, base_folder='results/extremes'):
    file_path = os.path.join(base_folder, name)

    with open(file_path, 'rb') as file:
        file_results = pickle.load(file)

    return file_results

def get_extremes_info(extremes):
    return extremes['info']

def get_extremes_data(extremes):
    return extremes['data']

def get_extremes_worst_point(extremes):
    return extremes['data']['worst_point']

def get_extremes_nondominated_population(extremes):
    return extremes['data']['nondominated_population']