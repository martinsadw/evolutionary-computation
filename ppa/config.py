def get_config():
    config = {}

    config['num_iterations'] = 5

    config['population_size'] = 5

    config['follow_distance_parameter'] = 1
    config['follow_survival_parameter'] = 1

    config['min_steps'] = 3
    config['max_steps'] = 3
    config['steps_distance_parameter'] = 1

    config['local_search_tries'] = 5

    config['follow_chance'] = 0.8

    return config


def get_config_ga():
    config = {}

    config['population_size'] = 20
    config['num_generations'] = 100

    config['top_selection_ratio'] = 0.2
    config['bottom_selection_ratio'] = 0.1
    config['mutation_chance'] = 0.01

    return config
