import random

RANDOM_SELECTION = 0

# TODO(andre:06-04-2018): Remover parametro quant

def selection_gene(population, quant, method, args):
	parents = ()

	if (method == RANDOM_SELECTION):
		parents = _random_selection_gene(population, quant, args)

	return parents

def _random_selection_gene(population, quant, args):
	parents = []

	for x in range(quant):
		parents.append(population[random.randrange(len(population))])

	return parents

# def _roulette_selection_gene(population, quant, args):
# def _stochastic_selection_gene(population, quant, args):
# def _truncation_selection_gene(population, quant, args):
