class Concept:
    def __init__(self, name='', abbreviation=''):
        self.name = name
        self.abbreviation = abbreviation

        self.id = 0
        self.prerequisites = None
        self.learning_materials = None
        self.level = 0

    def __str__(self):
        return "Concept{name=" + self.name + ", abbreviation=" + self.abbreviation + "}"
