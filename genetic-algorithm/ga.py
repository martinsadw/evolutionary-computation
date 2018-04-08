from ga_copying import *
from ga_selection import *
from ga_crossover import *
from ga_mutation import *
from ga_utils import *

# https://en.wikipedia.org/wiki/Genetic_algorithm
# https://watchmaker.uncommons.org/manual/ch03.html

def genetic_algorithm(fitness_func, config):
	population = []

	selection_quant = 2
	if (config['crossover_method'] == THREE_PARENT_CROSSOVER):
		selection_quant = 3

	for x in range(config['population_size']):
		population.append(random.randrange(0, config['gene_max']))

	for x in range(config['num_generations']):
		list.sort(population, key=fitness_func)

		new_population = copying_gene(population, config['copying_method'], config)

		remaining_spots = config['population_size'] - len(new_population)

		while remaining_spots > 0:
			parents = selection_gene(population, selection_quant, config['selection_method'], config)
			children = crossover_gene(parents, config['crossover_method'], config)

			for child in children:
				if remaining_spots > 0:
					child = mutation_gene(child, config['mutation_method'], config)

					remaining_spots -= 1
					new_population.append(child)
				else:
					break

		population = new_population

	list.sort(population, key=fitness)

	return population


config = {}
config['copying_method'] = PERMISSIVE_COPYING
config['selection_method'] = RANDOM_SELECTION
config['crossover_method'] = THREE_PARENT_CROSSOVER
config['mutation_method'] = BIT_INVERSION_MUTATION

config['gene_bitsize'] = 16
config['gene_max'] = 2 ** config['gene_bitsize']
config['precision_bitsize'] = 6

config['population_size'] = 100
config['num_generations'] = 10

config['top_selection_ratio'] = 0.2
config['bottom_selection_ratio'] = 0.1
config['mutation_chance'] = 0.001

result = genetic_algorithm(fitness, config)

print("Melhor resultado: " + str_gene(result[0]) + " -> " + str(fitness(result[0])))

gene = Gene(40, 16, 6)
print(gene)

