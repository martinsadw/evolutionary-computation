class Concepts:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.abbreviation = ""
        self.prerequisites = []


def create_concepts_list():
    concepts_list = []

    new_concept = Concepts()
    new_concept.id = 0
    new_concept.name = "conceito teste I"
    new_concept.name = "c_tst_1"
    new_concept.prerequisites = []
    concepts_list.append(new_concept)

    new_concept = Concepts()
    new_concept.id = 1
    new_concept.name = "conceito teste II"
    new_concept.name = "c_tst_2"
    new_concept.prerequisites = [1]
    concepts_list.append(new_concept)

    return concepts_list
