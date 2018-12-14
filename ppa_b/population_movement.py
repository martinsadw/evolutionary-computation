import numpy as np

from utils.misc import hamming_distance

# TODO(andre:2018-05-29): Fazer com que as funcoes de movimento realizem o
# numero correto de passos. Atualmente os materiais que sao iguais aos materiais
# da direcao para a qual se esta se movendo contam como um passo mesmo que
# nenhuma mudanca seja realizada


def move_population_roulette(population, num_steps, roulette, roulette_population):
    new_population = np.copy(population)

    step_order = np.random.rand(population.shape[0], population.shape[1]).argsort()

    try:
        biggest_num_steps = int(np.max(num_steps))
    except ValueError:  # Caso follow_num_steps esteja vazio
        biggest_num_steps = 0

    for i in range(biggest_num_steps):
        still_moving_mask = (num_steps > i)

        still_moving_indices = np.where(still_moving_mask)[0]
        # TODO(andre:2018-05-28): Garantir que max_steps nunca é maior do que o numero de materiais
        materials_indices = step_order[still_moving_mask, i]

        still_moving_roulette = roulette[still_moving_mask]
        follow_individual = [still_moving_roulette[index].spin() for index in np.ndindex(still_moving_roulette.shape)]

        new_population[still_moving_indices, materials_indices] = roulette_population[follow_individual, materials_indices]

    return new_population


def move_population_direction(population, num_steps, direction):
    new_population = np.copy(population)

    step_order = np.random.rand(population.shape[0], population.shape[1]).argsort()

    try:
        biggest_num_steps = int(np.max(num_steps))
    except ValueError:  # Caso follow_num_steps esteja vazio
        biggest_num_steps = 0

    for i in range(biggest_num_steps):
        still_moving_mask = (num_steps > i)

        still_moving_indices = np.where(still_moving_mask)[0]
        # TODO(andre:2018-05-28): Garantir que max_steps nunca é maior do que o numero de materiais
        materials_indices = step_order[still_moving_mask, i]

        new_population[still_moving_indices, materials_indices] = direction[still_moving_indices, materials_indices]

    return new_population

def move_population_random(population, num_steps):
    directions = np.random.randint(2, size=population.shape, dtype=bool)
    new_population = move_population_direction(population, num_steps, directions)

    return new_population

def move_population_random_complement(population, num_steps, away_direction):
    directions = np.random.randint(2, size=population.shape, dtype=bool)
    complement_directions = ~directions

    distances = hamming_distance(directions, away_direction, axis=1)
    complement_distances = hamming_distance(complement_directions, away_direction, axis=1)

    farther_directions = np.where(np.repeat((distances > complement_distances)[:, np.newaxis], population.shape[1], axis=1), directions, complement_directions)

    new_population = move_population_direction(population, num_steps, farther_directions)

    return new_population

def move_population_local_search(population, fitness_function, max_steps, num_tries, instance, timer):
    best_survival_values = fitness_function(population, instance, timer)
    for i in range(num_tries):
        num_steps = np.round(max_steps * np.random.rand(population.shape[0]))
        temp_population = move_population_random(population, num_steps)
        temp_survival_values = fitness_function(temp_population, instance, timer)

        better_survival_values = (temp_survival_values < best_survival_values)
        population = np.where(np.repeat(better_survival_values[:, np.newaxis], population.shape[1], axis=1), temp_population, population)
        best_survival_values = np.where(better_survival_values, temp_survival_values, best_survival_values)

    return population
