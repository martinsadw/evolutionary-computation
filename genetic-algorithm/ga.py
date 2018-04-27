import time

from ga_copying import *
from ga_local_search import *
from ga_selection import *
from ga_crossover import *
from ga_mutation import *
from ga_config import *
from ga_gene import Gene


# https://en.wikipedia.org/wiki/Genetic_algorithm
# https://watchmaker.uncommons.org/manual/ch03.html

def genetic_algorithm(fitness_func, base_gene, args):
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

        if args['use_local_search']:
            local_search_gene(new_population, fitness_func, args['local_search_method'], args)

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


config = get_config()

base_gene = Gene()
base_gene.add_fixed("x", 16, 6)
base_gene.add_fixed("y", 16, 6)


def fitness(gene):
    x = gene.get_value("x")
    y = gene.get_value("y")

    # return x*x - 5*x + 4

    # 85.1326727 -> -4568.23409
    return 0.0001 * x ** 4 - 0.002 * x ** 3 - 1.2 * x ** 2 + 1 * x + 25 + y


start_time = time.time()
result = genetic_algorithm(fitness, base_gene, config)
print("Melhor resultado: (" + str(result[0].get_value("x")) + ", " + str(result[0].get_value("y")) + ") -> " + str(fitness(result[0])))
print("Tempo de execução: %.2fs" % (time.time() - start_time))
