from ga_copying import *
from ga_selection import *
from ga_crossover import *
from ga_mutation import *
from ga_gene import Gene

# https://en.wikipedia.org/wiki/Genetic_algorithm
# https://watchmaker.uncommons.org/manual/ch03.html

def new_genetic_algorithm(fitness_func, base_gene, args):
	population = []

	selection_quant = 2
	if (args['crossover_method'] == THREE_PARENT_CROSSOVER):
		selection_quant = 3

	for x in range(args['population_size']):
		new_gene = Gene.like(base_gene)

		for name in base_gene.variables:
			new_gene.set_bits(name, random.randrange(0, new_gene.get_variable_max(name)))

		population.append(new_gene)

	for x in range(args['num_generations']):
		list.sort(population, key=fitness_func)

		new_population = copying_gene(population, args['copying_method'], args)

		remaining_spots = args['population_size'] - len(new_population)

		while remaining_spots > 0:
			parents = selection_gene(population, selection_quant, args['selection_method'], args)
			children = crossover_gene(parents, args['crossover_method'], args)

			for child in children:
				if remaining_spots > 0:
					child = mutation_gene(child, args['mutation_method'], args)

					remaining_spots -= 1
					new_population.append(child)
				else:
					break

		population = new_population

	list.sort(population, key=fitness_func)

	return population

config = {}
config['copying_method'] = PERMISSIVE_COPYING
config['selection_method'] = RANDOM_SELECTION
config['crossover_method'] = THREE_PARENT_CROSSOVER
config['mutation_method'] = BIT_INVERSION_MUTATION

config['population_size'] = 1000
config['num_generations'] = 100

config['top_selection_ratio'] = 0.2
config['bottom_selection_ratio'] = 0.1
config['mutation_chance'] = 0.001

base_gene = Gene()
base_gene.add_fixed("x", 16, 6)

def new_fitness(gene):
	x = gene.get_value("x")

	# return x*x - 5*x + 4

	# 85.1326727 -> -4568.23409
	return 0.0001*x**4 - 0.002*x**3 - 1.2*x**2 + 1*x + 25

result = new_genetic_algorithm(new_fitness, base_gene, config)
print("Melhor resultado: " + str(result[0].get_value("x")) + " -> " + str(new_fitness(result[0])))
