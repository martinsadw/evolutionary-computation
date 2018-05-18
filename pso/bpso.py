import random
import numpy as np

def get_integer(array):
	total = 0
	for shift, bit in enumerate(array[::-1]):
		total += bit * (1 << shift)
	return total

def get_float(array, bits_precision):
	total = 0
	for shift, bit in enumerate(array[::-1]):
		total += bit * (1 << shift)
	return (total / (1 << bits_precision))

def sigmoid(x):
	return 1 / (1 + np.exp(-x));

def fitness(array):
	# x = get_float(array[4:8], 0)
	# y = get_float(array[0:4], 0)

	x = get_float(array[16:32], 10)
	y = get_float(array[0:16], 10)

	return x**2 + y**2 - 4*x*y + 0.2*(x**2)*(y**2)

v_max = 2
particle_size = 32
num_particles = 50
num_iterations = 100
param_a = 1.0
param_b = 0.3
param_c = 0.2

p_velocity = np.random.rand(num_particles, particle_size) * (2 * v_max) - v_max
p_sigmoid = sigmoid(p_velocity)
p_random = np.random.random(p_velocity.shape)
p_position = (p_sigmoid > p_random).astype(int)

p_best_position = p_position[:]
p_best_result = np.apply_along_axis(fitness, 1, p_best_position)

g_best_index = np.argmin(p_best_result, axis=0)
g_best_position = p_best_position[g_best_index]
g_best_result = p_best_result[g_best_index]

# print(p_best_position)
# print(p_best_result)
# print(g_best_position)
# print(g_best_result)

for i in range(num_iterations):
	# TODO(andre:2018-04-18): Atualizar velocidade
	p_influence = np.tile(param_b * np.random.random(num_particles), (particle_size, 1)).T
	g_influence = np.tile(param_c * np.random.random(num_particles), (particle_size, 1)).T

	p_velocity = param_a * p_velocity + p_influence * (p_best_position - p_position) + g_influence * (g_best_position - p_position)
	p_velocity = np.clip(p_velocity, -v_max, v_max)

	# Calcula as novas posições
	p_new_sigmoid = sigmoid(p_velocity)
	p_new_random = np.random.random(p_velocity.shape)
	p_position = (p_new_sigmoid > p_new_random).astype(int)

	# Calcula os novos resultados
	p_new_result = np.apply_along_axis(fitness, 1, p_position)

	# Calcula a mascara de melhores valores para cada particula
	change_mask = (p_new_result < p_best_result)

	# Altera o melhor resultado de cada particula
	p_best_result[change_mask] = p_new_result[change_mask]
	p_best_position[change_mask] = p_position[change_mask]

	# Encontra o melhor resultado entre todas as particulas
	g_best_index = np.argmin(p_best_result, axis=0)
	g_best_position = p_best_position[g_best_index]
	g_best_result = p_best_result[g_best_index]

# print(p_best_position)
# print(p_best_result)
# print(g_best_position)
# print(g_best_result)

x = get_float(g_best_position[16:32], 10)
y = get_float(g_best_position[0:16], 10)
print("Melhor resultado: (" + str(x) + ", " + str(y) + ") -> " + str(g_best_result))
