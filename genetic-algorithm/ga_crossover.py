import random

SINGLE_POINT_CROSSOVER = 0
TWO_POINT_CROSSOVER = 1
THREE_PARENT_CROSSOVER = 2
UNIFORM_CROSSOVER = 3

def crossover_gene(genes, method, args):
	new_gene = genes[0]

	if (method == SINGLE_POINT_CROSSOVER):
		new_gene = _single_point_crossover_gene(genes, args)

	elif (method == TWO_POINT_CROSSOVER):
		new_gene = _two_point_crossover_gene(genes, args)

	elif (method == THREE_PARENT_CROSSOVER):
		new_gene = _three_parent_crossover_gene(genes, args)

	elif (method == UNIFORM_CROSSOVER):
		new_gene = _uniform_crossover_gene(genes, args)

	return new_gene

def _single_point_crossover_gene(genes, args):
	assert len(genes) == 2
	assert 'gene_bitsize' in args

	cut_point = random.randrange(1, args['gene_bitsize'])

	mask = (2 ** cut_point) - 1 # e.g. 0000 0000 0011 1111 se cut_point = 6

	gene1 = (genes[0] & ~mask) | (genes[1] &  mask)
	gene2 = (genes[0] &  mask) | (genes[1] & ~mask)

	return (gene1, gene2)

def _two_point_crossover_gene(genes, args):
	assert len(genes) == 2
	assert 'gene_bitsize' in args

	# TODO(andre:2018-04-05): Garantir que os pontos de cortes sejam diferentes
	cut_point1 = random.randrange(1, args['gene_bitsize'])
	cut_point2 = random.randrange(1, args['gene_bitsize'])

	mask1 = (2 ** cut_point1) - 1 # e.g. 0000 0000 0011 1111 se cut_point1 = 6
	mask2 = (2 ** cut_point2) - 1 # e.g. 0000 0111 1111 1111 se cut_point2 = 11
	mask = (mask1 ^ mask2)        # e.g. 0000 0111 1100 0000

	gene1 = (genes[0] & ~mask) | (genes[1] &  mask)
	gene2 = (genes[0] &  mask) | (genes[1] & ~mask)

	return (gene1, gene2)

def _three_parent_crossover_gene(genes, args):
	assert len(genes) == 3

	# Exemplo:
	# genes[0]:         110100010
	# genes[1]:         011001001
	# genes[2]:         110110101

	# mask:             010010100

	# genes[0] &  mask: 010000000
	# genes[2] & ~mask: 100100001
	# gene:             110100001

	mask = ~(genes[0] ^ genes[1]) # seleciona os bits que são iguais

	new_gene = (genes[0] & mask) | (genes[2] & ~mask) # usa o terceiro pai em caso de empate

	return (new_gene,)

def _uniform_crossover_gene(genes, args):
	assert len(genes) == 2

	new_gene = genes[0]

	for x in range(gene_bitsize):
		if random.random() < 0.5:
			new_gene |= genes[1] & (1 << x)

	return (new_gene,)
