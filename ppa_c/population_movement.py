import numpy as np

from utils.misc import sigmoid, vector_size, random_on_unit_sphere, improve_population


def move_population_direction(population, num_steps, direction):
    new_population = np.copy(population)
    direction = direction / vector_size(direction)[:, np.newaxis]

    new_population += direction * num_steps[:, np.newaxis]

    return new_population


def move_population_random(population, num_steps):
    directions = random_on_unit_sphere((population.shape[0],), population.shape[1])
    # directions = np.random.randint(2, size=population.shape, dtype=bool)
    new_population = move_population_direction(population, num_steps, directions)

    return new_population


def move_population_random_complement(population, num_steps, away_direction):
    directions = random_on_unit_sphere((population.shape[0],), population.shape[1])

    distances = vector_size(away_direction - (population + directions), axis=1)
    complement_distances = vector_size(away_direction - (population - directions), axis=1)

    farther_directions = np.where(np.repeat((distances > complement_distances)[:, np.newaxis], population.shape[1], axis=1), directions, -directions)

    new_population = move_population_direction(population, num_steps, farther_directions)

    return new_population


def move_population_local_search(population, fitness_function, evaluate_function, max_steps, num_tries, instance, timer):
    population_evaluation = evaluate_function(population)
    best_survival_values = fitness_function(population_evaluation, instance, timer)
    for i in range(num_tries):
        num_steps = np.round(max_steps * np.random.rand(population.shape[0]))
        temp_population = move_population_random(population, num_steps)
        temp_population_evaluation = evaluate_function(temp_population)
        temp_survival_values = fitness_function(temp_population_evaluation, instance, timer)

        (population, best_survival_values) = improve_population(population, best_survival_values, temp_population, temp_survival_values)

    return population
