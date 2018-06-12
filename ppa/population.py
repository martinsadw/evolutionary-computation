# TODO Mudar (talvez) representação de vetor de inteiros pra um único inteiro em binário


class Population:
    def __init__(self, individuals=None):
        self.individuals = individuals

        self.size_population = 0
        self.best_preys_id = None
        self.predator_id = 0
        self.ordinary_preys_ids = None

    def __str__(self):
        returned = ''
        for individual in self.individuals:
            returned += 'ID = ' + str(individual.id) + '\n'
            for position in individual.prey:
                returned += str(position) + ' '
            returned += '\n'
            returned += 'Survival value = ' + str(individual.survival_value) + '\n'
        returned += '\nBest prey = ' + str(self.best_preys_id) + '\n'
        returned += 'Predator = ' + str(self.predator_id) + '\n'
        returned += 'Ordinary preys = ' + str(self.ordinary_preys_ids) + '\n'

        return returned
