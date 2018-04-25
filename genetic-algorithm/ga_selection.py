import random
import math

RANDOM_SELECTION = 0
ROULETTE_SELECTION = 1


# TODO(andre:06-04-2018): Remover parametro quant

def selection_gene(population, quant, method, args):
    parents = ()

    if method == RANDOM_SELECTION:
        parents = _random_selection_gene(population, quant, args)

    elif method == ROULETTE_SELECTION:
        parents = _roulette_selection_gene(population, quant)

    return parents


def _random_selection_gene(population, quant, args):
    parents = []

    for x in range(quant):
        parents.append(population[random.randrange(len(population))])

    return parents


def _roulette_selection_gene(population, quant):
    parents = []

    # Cada elemento i da população terá (len(population) - i) de chance de ser selecionado (peso na roleta)
    # ex.: Peso de population[0] = len(population)
    #      Peso de parents[1] = len(population) - 1
    #      ...
    #      Peso de parents[len(population) - 2] = 2
    #      Peso de parents[len(population) - 1] = 1

    # Logo, o peso total da roleta é o somatório de 1 a len(population):
    total_weight = int((len(population) + 1) * len(population) / 2)

    for x in range(quant):
        roulette = random.randint(1, total_weight)

        # Isolando o peso na fórmula do somatório:
        #
        # roulette = (weight + 1) * weight / 2
        # weight * (weight + 1) = 2 * roulette
        # weight ** 2 + w - 2 * roulette = 0
        weight = math.ceil((-1 + math.sqrt(1 + 8 * roulette)) / 2)

        # Como weight = len(population) - i:
        i = len(population) - weight

        parents.append(population[i])

    return parents




# def _stochastic_selection_gene(population, quant, args):
# def _truncation_selection_gene(population, quant, args):
