import random

# TODO Mudar (talvez) representação de vetor de inteiros pra um único inteiro em binário


class Individual:
    def __init__(self, paramId, size):
        self.size = size
        self.id = paramId
        self.prey = [0] * self.size

        self.survival_value = 0.0

    def generate_random_prey(self):
        self.prey.clear()
        for i in range(self.size):
            self.prey.append(random.randint(0, 1))

    def __str__(self):
        returned = ''
        for position in self.prey:
            returned += str(position) + ' '
        return returned + '\nSurvival value: ' + str(self.survival_value) + '\n'
