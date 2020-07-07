import os


def results_name(algorithm, instance):
    return ('%s_%s' % (algorithm, instance))


def open_results(algorithm, instance, base_folder='results/algorithm_results'):
    file_path = os.path.join(base_folder, results_name(algorithm, instance))

    with open(file_path, 'rb') as file:
        file_results = pickle.load(file)

    return file_results


def get_results_info(results):
    return results['info']

def get_results_instance(results):
    return results['info']['instance']

def get_results_data(results):
    return results['data']

def get_results_selected_materials(results):
    return results['data'][0]

def get_results_cost(results):
    return results['data'][1]

def get_results_best(results):
    # if results['info']['format'] != 'full':
    #     raise Exception('List of best results is only present in the "full" format')

    return results['data'][2]

def get_results_population_fitness(results):
    return results['data'][3]
