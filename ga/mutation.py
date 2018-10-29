import random
from enum import Enum
import numpy as np

class Mutation(Enum):
    BIT_INVERSION_MUTATION = 1


def mutation_gene(children, method, config):
    new_gene=np.copy(children)

    if (method == Mutation.BIT_INVERSION_MUTATION):
        new_gene = _bit_inversion_mutation_gene(children, config)
    return new_gene


def _bit_inversion_mutation_gene(children, config):
    new_gene=np.copy(children)
    bitsize = children.shape[1]
    for g in new_gene:
        mask = np.zeros(bitsize,dtype=bool)
        for x in range(bitsize):
            if random.random() <  config.mutation_chance:
                mask[x]=True
       
        g ^= mask

    return new_gene
