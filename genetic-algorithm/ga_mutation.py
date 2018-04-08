import random

BIT_INVERSION_MUTATION = 0

def mutation_gene(gene, method, args):
	new_gene = gene

	if (method == BIT_INVERSION_MUTATION):
		new_gene = _bit_inversion_mutation_gene(gene, args)

	return gene

def _bit_inversion_mutation_gene(gene, args):
	assert 'gene_bitsize' in args
	assert 'mutation_chance' in args

	for x in range(args['gene_bitsize']):
		if random.random() < args['mutation_chance']:
			gene ^= (1 << x)

	return gene
	
