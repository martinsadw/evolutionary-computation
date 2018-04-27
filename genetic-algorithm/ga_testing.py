from ga_copying import *
from ga_selection import *
from ga_crossover import *
from ga_mutation import *
from ga_config import *
from ga_gene import Gene


config = get_config()

output = open(OUTPUT_FILENAME, "w")

output.write("Metodo de copia dos genes: ")

if config['copying_method'] == ELITISM_COPYING:
    output.write("Elitismo")
elif config['copying_method'] == PERMISSIVE_COPYING:
    output.write("Permissivo (copia parte dos melhores e parte dos piores genes)")
elif config['copying_method'] == NO_COPYING:
    output.write("Nao copia")

output.write("\n")

output.write("Metodo de crossover: ")

if config['crossover_method'] == SINGLE_POINT_CROSSOVER:
    output.write("Crossover de 1 ponto")
elif config['crossover_method'] == TWO_POINT_CROSSOVER:
    output.write("Crossover de 2 pontos")
elif config['crossover_method'] == THREE_PARENT_CROSSOVER:
    output.write("Crossover de 3 pais")
elif config['crossover_method'] == UNIFORM_CROSSOVER:
    output.write("Crossover uniforme")
elif config['crossover_method'] == DECIMAL_CROSSOVER:
    output.write("Crossover entre parte inteira e decimal")

output.write("\n")

output.write("Metodo de selecao de pais: ")

if config['selection_method'] == RANDOM_SELECTION:
    output.write("Selecao aleatoria")
elif config['selection_method'] == ROULETTE_SELECTION:
    output.write("Selecao por roleta")

output.write("\n")

output.write("Tamanho da populacao: {}\n".format(config['population_size']))
output.write("Numero de geracoes: {}\n".format(config['num_generations']))

if config['copying_method'] != NO_COPYING:
    output.write("Taxa de selecao dos melhores genes: {}\n".format(config['top_selection_ratio']))

if config['copying_method'] == PERMISSIVE_COPYING:
    output.write("Taxa de selecao dos piores genes: {}\n".format(config['bottom_selection_ratio']))

output.write("Chance de mutacao: {}\n\n\n".format(config['mutation_chance']))


def new_genetic_algorithm(fitness_func, base_gene, args, output):
    population = []

    selection_quant = 2
    if args['crossover_method'] == THREE_PARENT_CROSSOVER:
        selection_quant = 3

    for x in range(args['population_size']):
        new_gene = Gene.like(base_gene)

        for name in base_gene.variables:
            new_gene.set_bits(name, random.randrange(0, new_gene.get_variable_max(name)))

        population.append(new_gene)

    for x in range(args['num_generations']):
        list.sort(population, key=fitness_func)

        # Imprime a população de cada geração
        output.write("Populacao da {}a geracao:\n".format(x+1))
        for gene in population:
            output.write("{} -> {}\n".format(gene.get_value("x"), new_fitness(gene)))
        output.write("\n")
        # </> Imprime a população de cada geração

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


def raw_fitness(x):
    # return x*x - 5*x + 4

    # 85.1326727 -> -4568.23409
    return 0.0001 * x ** 4 - 0.002 * x ** 3 - 1.2 * x ** 2 + 1 * x + 25


def new_fitness(gene):
    x = gene.get_value("x")

    # return x*x - 5*x + 4

    # 85.1326727 -> -4568.23409
    return 0.0001 * x ** 4 - 0.002 * x ** 3 - 1.2 * x ** 2 + 1 * x + 25


base_gene = Gene()
base_gene.add_fixed("x", 16, 6)

average_x = 0
best_x = 0
premature_convergences = 0

output.write("Resultados:\n")

for i in range(NUM_ITERATIONS):
    print("Processando {} de {}...".format(i + 1, NUM_ITERATIONS))

    result = new_genetic_algorithm(new_fitness, base_gene, config, output)

    output.write("{} -> {}\n".format(result[0].get_value("x"), new_fitness(result[0])))

    if i == 0:
        best_x = result[0].get_value("x")

    elif new_fitness(result[0]) < raw_fitness(best_x):
        best_x = result[0].get_value("x")

    if result[0].get_value("x") < 0:
        premature_convergences += 1

    average_x += result[0].get_value("x")

average_x /= NUM_ITERATIONS

output.write("\nMelhor solucao: {} -> {}\n".format(best_x, raw_fitness(best_x)))
output.write("Solucao media: {} -> {}\n".format(average_x, raw_fitness(average_x)))
output.write("\nNumero de convergencias para o minimo local: {}\n".format(premature_convergences))
output.write("\nSolucao ideal (minimo global): 85.1326727 -> -4568.23409\n")
output.write("Minimo local: -70.5493 -> -2838.66\n")

output.close()

print("Concluido")
