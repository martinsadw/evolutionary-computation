import random
from ga_gene import Gene

SINGLE_POINT_CROSSOVER = 0
TWO_POINT_CROSSOVER = 1
THREE_PARENT_CROSSOVER = 2
UNIFORM_CROSSOVER = 3
DECIMAL_CROSSOVER = 4


def crossover_gene(genes, method, args):
    new_gene = genes[0]

    if method == SINGLE_POINT_CROSSOVER:
        new_gene = _single_point_crossover_gene(genes, args)

    elif method == TWO_POINT_CROSSOVER:
        new_gene = _two_point_crossover_gene(genes, args)

    elif method == THREE_PARENT_CROSSOVER:
        new_gene = _three_parent_crossover_gene(genes, args)

    elif method == UNIFORM_CROSSOVER:
        new_gene = _uniform_crossover_gene(genes, args)

    elif method == DECIMAL_CROSSOVER:
        precision = new_gene.variables_descriptor['x'][2]
        new_gene = _single_point_crossover_gene(genes, args, precision)

    return new_gene


def _single_point_crossover_gene(genes, args, cut_point = None):
    assert len(genes) == 2

    # Exemplo:
    # value1:         1101 0011
    # value2:         1001 1101

    # cut_point: 5

    # mask:           0001 1111

    # value1 & ~mask: 1100 0000
    # value2 &  mask: 0001 1101
    # result1:        1101 1101

    # value1 &  mask: 0001 0011
    # value2 & ~mask: 1000 0000
    # result2:        1001 0011

    new_gene1 = Gene.like(genes[0])
    new_gene2 = Gene.like(genes[0])

    for name in new_gene1.variables:
        value1 = genes[0].variables[name]
        value2 = genes[1].variables[name]

        if cut_point is None:
            bitsize = new_gene1.get_variable_size(name)
            cut_point = random.randrange(1, bitsize)

        mask = (1 << cut_point) - 1  # e.g. 0000 0000 0011 1111 se cut_point = 6

        new_gene1.variables[name] = (value1 & ~mask) | (value2 & mask)
        new_gene2.variables[name] = (value1 & mask) | (value2 & ~mask)

    return (new_gene1, new_gene2)


def _two_point_crossover_gene(genes, args):
    assert len(genes) == 2

    # Exemplo:
    # value1:         1101 0011
    # value2:         1001 1101

    # cut_point1: 3
    # cut_point2: 7

    # mask1:          0000 0111
    # mask2:          0111 1111
    # mask:           0111 1000

    # value1 & ~mask: 1000 0011
    # value2 &  mask: 0001 1000
    # result1:        1001 1011

    # value1 &  mask: 0101 0000
    # value2 & ~mask: 1000 0101
    # result2:        1101 0101

    new_gene1 = Gene.like(genes[0])
    new_gene2 = Gene.like(genes[0])

    for name in new_gene1.variables:
        bitsize = new_gene1.get_variable_size(name)

        value1 = genes[0].variables[name]
        value2 = genes[1].variables[name]

        # TODO(andre:2018-04-05): Garantir que os pontos de cortes sejam diferentes
        cut_point1 = random.randrange(1, bitsize)
        cut_point2 = random.randrange(1, bitsize)

        mask1 = (1 << cut_point1) - 1  # e.g. 0000 0000 0011 1111 se cut_point1 = 6
        mask2 = (1 << cut_point2) - 1  # e.g. 0000 0111 1111 1111 se cut_point2 = 11
        mask = (mask1 ^ mask2)         # e.g. 0000 0111 1100 0000

        new_gene1.variables[name] = (value1 & ~mask) | (value2 & mask)
        new_gene2.variables[name] = (value1 & mask) | (value2 & ~mask)

    return (new_gene1, new_gene2)


def _three_parent_crossover_gene(genes, args):
    assert len(genes) == 3

    # Exemplo:
    # value1:         110100010
    # value2:         011001001
    # value3:         110110101

    # mask:           010010100

    # value1 &  mask: 010000000
    # value3 & ~mask: 100100001

    # result:         110100001

    new_gene = Gene.like(genes[0])

    for name in new_gene.variables:
        value1 = genes[0].variables[name]
        value2 = genes[1].variables[name]
        value3 = genes[2].variables[name]

        mask = ~(value1 ^ value2)  # seleciona os bits que sao iguais

        new_gene.variables[name] = (value1 & mask) | (value3 & ~mask)  # usa o terceiro pai em caso de empate

    return (new_gene,)


def _uniform_crossover_gene(genes, args):
    assert len(genes) == 2

    # Exemplo:
    # value1:         1101 0011
    # value2:         1001 1101

    # mask:           0010 0110

    # value1 & ~mask: 1101 0001
    # value2 &  mask: 0000 0100

    # result:         1101 0101

    new_gene = Gene.like(genes[0])

    for name in new_gene.variables:
        value1 = genes[0].variables[name]
        value2 = genes[1].variables[name]
        bitsize = new_gene.get_variable_size(name)

        mask = 0
        for x in range(bitsize):
            if random.random() < 0.5:
                mask &= (1 << x)

        new_gene.variables[name] = (value1 & ~mask) | (value2 & mask)

    return (new_gene,)
