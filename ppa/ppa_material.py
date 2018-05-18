class Material:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.learning_time = 0
        self.difficulty = ""
        self.types = []
        self.interactivity_level = ""
        self.interactivity_type = ""

        # self.covered_concepts = []

        self.active_value = 0
        self.reflexive_value = 0
        self.sensory_value = 0
        self.intuitive_value = 0
        self.visual_value = 0
        self.verbal_value = 0
        self.sequential_value = 0
        self.global_value = 0


def create_materials_list():
    material_list = []

    new_material = Material()
    new_material.id = 0
    new_material.name = "material teste I"
    new_material.learning_time = 10 * 60
    new_material.difficulty = "medium"
    new_material.types = ["slide"]
    new_material.interactivity_level = "very low"
    new_material.interactivity_type = "expositive"
    material_list.append(new_material)

    new_material = Material()
    new_material.id = 1
    new_material.name = "material teste II"
    new_material.learning_time = 10 * 60
    new_material.difficulty = "medium"
    new_material.types = ["slide"]
    new_material.interactivity_level = "very low"
    new_material.interactivity_type = "expositive"
    material_list.append(new_material)

    return material_list
