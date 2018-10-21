import random
from enum import Enum

class Mutation(Enum):
    BIT_INVERSION_MUTATION = 1


def mutation_gene(gene, method, args):
    new_gene = gene

    if (method == Mutation.BIT_INVERSION_MUTATION):
        new_gene = _bit_inversion_mutation_gene(gene, args)

    return new_gene

def _bit_inversion_mutation_gene(gene, args):
    assert 'mutation_chance' in args

    new_gene =gene

    for name in new_gene.variables:
        bitsize = new_gene.get_variable_size(name)

        mask = 0
        for x in range(bitsize):
            if random.random(0,100) < args['mutation_chance']:
                mask &= (1 << x)

        new_gene.variables[name] ^= mask

    return new_gene
