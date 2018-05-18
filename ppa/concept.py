class Concept:
    def __init__(self, name='', abbreviation=''):
        self.name = name
        self.abbreviation = abbreviation

        self.id = 0
        self.prerequisites = None
        self.LMs = None
        self.level = 0
