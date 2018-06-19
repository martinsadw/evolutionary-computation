import numpy as np

from objective import fitness_population
from utils import hamming_distance

# TODO(andre:2018-05-29): Fazer com que as funcoes de movimento realizem o
# numero correto de passos. Atualmente os materiais que sao iguais aos materiais
# da direcao para a qual se esta se movendo contam como um passo mesmo que
# nenhuma mudanca seja realizada


def move_population_roulette(population, num_steps, roulette, roulette_population, mask):
    new_population = np.copy(population)

    step_order = np.random.rand(population.shape[0], population.shape[1]).argsort()

    # print('New population:\n{}\n'.format(new_population))
    # print('Step order:\n{}\n'.format(step_order))
    # print('Num steps:\n{}\n'.format(num_steps))
    # print('Mask:\n{}\n'.format(mask))
    try:
        biggest_num_steps = int(np.max(num_steps[mask]))
    except ValueError: # Caso follow_num_steps esteja vazio
        biggest_num_steps = 0

    for i in range(biggest_num_steps):
        still_moving_mask = ((num_steps > i) & mask)

        still_moving_indices = np.where(still_moving_mask)[0]
        # TODO(andre:2018-05-28): Garantir que max_steps nunca é maior do que o numero de materiais
        materials_indices = step_order[still_moving_mask, i]

        still_moving_roulette = roulette[still_moving_mask]
        follow_individual = np.empty(still_moving_roulette.shape, dtype=int)
        for index in np.ndindex(still_moving_roulette.shape):
            follow_individual[index] = still_moving_roulette[index].spin()

        # print('-----------------------------' + str(i))
        # print('Still moving population:\n{}\n'.format(new_population[still_moving_mask]))
        # print('Materials to change:\n{}\n'.format(new_population[still_moving_indices, materials_indices]))
        # print('Materials to assign:\n{}\n'.format(roulette_population[follow_individual, materials_indices]))
        # print('Follow individual:\n{}\n'.format(follow_individual))

        # print('Unchanged population:\n{}\n'.format(new_population))
        new_population[still_moving_indices, materials_indices] = roulette_population[follow_individual, materials_indices]

    return new_population


def move_population_direction(population, num_steps, direction, mask):
    new_population = np.copy(population)

    step_order = np.random.rand(population.shape[0], population.shape[1]).argsort()

    try:
        biggest_num_steps = int(np.max(num_steps[mask]))
    except ValueError: # Caso follow_num_steps esteja vazio
        biggest_num_steps = 0

    for i in range(biggest_num_steps):
        still_moving_mask = ((num_steps > i) & mask)

        still_moving_indices = np.where(still_moving_mask)[0]
        # TODO(andre:2018-05-28): Garantir que max_steps nunca é maior do que o numero de materiais
        materials_indices = step_order[still_moving_mask, i]

        new_population[still_moving_indices, materials_indices] = direction[still_moving_indices, materials_indices]

    return new_population


def move_population_random(population, num_steps, mask):
    directions = np.random.randint(2, size=population.shape, dtype=bool)
    # print('Random direction:\n{}\n'.format(direction))
    new_population = move_population_direction(population, num_steps, directions, mask)

    return new_population


def move_population_random_complement(population, num_steps, away_direction, mask):
    directions = np.random.randint(2, size=population.shape, dtype=bool)
    complement_directions = ~directions

    distances = hamming_distance(directions, away_direction, axis=1)
    complement_distances = hamming_distance(complement_directions, away_direction, axis=1)

    farther_directions = np.where(np.repeat((distances > complement_distances)[:, np.newaxis], population.shape[1], axis=1), directions, complement_directions)
    # print('Away direction:\n{}\n'.format(away_direction))
    # print('Random direction:\n{}\n'.format(directions))
    # print('Complement direction:\n{}\n'.format(complement_directions))
    # print('Random distance:\n{}\n'.format(distances))
    # print('Complement distance:\n{}\n'.format(complement_distances))
    # print('Farther direction:\n{}\n'.format(farther_direction))
    new_population = move_population_direction(population, num_steps, farther_directions, mask)

    return new_population

def move_population_local_search(population, mask, max_steps, num_tries, instance):
    best_population = np.copy(population)
    best_survival_values = fitness_population(best_population, instance)
    for i in range(num_tries):
        # print('-----------------------------' + str(i))
        num_steps = np.round(max_steps * np.random.rand(population.shape[0]))
        temp_population = move_population_random(population, num_steps, mask)
        temp_survival_values = fitness_population(temp_population, instance)

        # print('Temp population:\n{}\n'.format(temp_population))
        # print('Temp survival values:\n{}\n'.format(temp_survival_values))

        better_survival_values = (temp_survival_values < best_survival_values)
        best_population = np.where(np.repeat(better_survival_values[:, np.newaxis], population.shape[1], axis=1), temp_population, best_population)
        best_survival_values = np.where(better_survival_values, temp_survival_values, best_survival_values)
        # print('Partial best population:\n{}\n'.format(best_population))
        # print('Partial best survival values:\n{}\n'.format(best_survival_values))

    return best_population
