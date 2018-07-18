class Concept:
    def __init__(self, name='', abbreviation=''):
        self.name = name
        self.abbreviation = abbreviation

        self.id = 0
        self.prerequisites = None
        self.learning_materials = None
        self.level = 0

    @classmethod
    def load_from_string(cls, description):
        fields = description.split(';')

        abbreviation = fields[0]
        concept_name = fields[1]

        return cls(concept_name, abbreviation)

    def __str__(self):
        return "Concept{name=" + self.name + ", abbreviation=" + self.abbreviation + "}"
