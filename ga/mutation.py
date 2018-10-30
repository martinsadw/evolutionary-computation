import random
from enum import Enum
import numpy as np

class Mutation(Enum):
    BIT_INVERSION_MUTATION = 1
    SINGLE_INVERSION_MUTATION=2


def mutation_gene(children, method, config):
    new_gene=np.copy(children)

    if (method == Mutation.BIT_INVERSION_MUTATION):
        new_gene = _bit_inversion_mutation_gene(children, config)
    if (method==Mutation.SINGLE_INVERSION_MUTATION):
        new_gene=_single_bit_mutation(children,config)
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

def _single_bit_mutation(children,config,bit=None):
    new_gene=np.copy(children)
    bitsize=children.shape[1]
    for g in new_gene:
        if random.random()<config.mutation_chance:
            bitPos=np.random.randint(0,bitsize)
            if(g[bitPos]==True):
                g[bitPos]=False
            else:
                g[bitPos]=True
    return new_gene