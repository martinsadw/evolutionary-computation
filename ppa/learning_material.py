class LearningMaterial:
    # TODO(andre:2018-05-19): Permitir criar um instancia de LearningMaterial
    # passando uma string com o nome do arquivo LOM com as informacoes do material
    def __init__(self, param_id, name, param_type, typical_learning_time, difficulty, learning_resource_types, interativity_level, interativity_type):
        learning_resource_type_possible_active_values = ['exercise', 'simulation', 'questionnaire', 'test', 'experiment']
        learning_resource_type_possible_reflexive_values = ['simulation', 'diagram', 'figure', 'graphic', 'slide', 'table', 'narrative text', 'test', 'problems declaration']

        learning_resource_type_possible_sensory_values = ["exercise", "simulation", "graphic", "slide", "test", "table", "narrative text", "experiment", "problems declaration"]
        learning_resource_type_possible_intuitive_values = ["simulation", "questionnaire", "diagram", "test", "figure", "slide", "narrative text"]

        learning_resource_type_possible_visual_values = ["simulation", "diagram", "figure", "graphic", "slide", "table"]
        learning_resource_type_possible_verbal_values = ["slide", "narrative text", "reading"]

        learning_resource_type_possible_sequential_values = ["exercise", "simulation", "diagram", "slide", "narrative text", "experiment"]
        learning_resource_type_possible_global_values = ["diagram", "figure", "graphic", "slide", "table", "narrative text"]

        self.id = param_id
        self.name = name
        self.type = param_type

        if difficulty == "very difficult":
            self.difficulty = 5.0
        elif difficulty == "difficult":
            self.difficulty = 4.0
        elif difficulty == "easy":
            self.difficulty = 2.0
        elif difficulty == "very easy":
            self.difficulty = 1.0
        elif difficulty == "medium":
            self.difficulty = 3.0
        else:
            print("Dificuldade não mapeada: {}".format(difficulty))
            self.difficulty = 0.0

        hour = 0
        minute = 0
        second = 0

        # TODO(andre:2018-05-19): Considerar usar expressoes regulares para obter a duracao do material
        typical_learning_time = typical_learning_time.replace("PT", "")
        if "H" in typical_learning_time:
            hour = int(typical_learning_time.split("H")[0])
            if len(typical_learning_time.split("H")) == 2:
                typical_learning_time = typical_learning_time.split("H")[1]

        if "M" in typical_learning_time:
            minute = int(typical_learning_time.split("M")[0])
            if len(typical_learning_time.split("M")) == 2:
                typical_learning_time = typical_learning_time.split("M")[1]

        if "S" in typical_learning_time:
            second = int(typical_learning_time.replace("S", "")[0])

        self.typical_learning_time = (hour * 3600) + (minute * 60) + second

        self.learning_style_active_value = 0
        self.learning_style_reflexive_value = 0
        self.learning_style_sensory_value = 0
        self.learning_style_intuitive_value = 0
        self.learning_style_visual_value = 0
        self.learning_style_verbal_value = 0
        self.learning_style_sequential_value = 0
        self.learning_style_global_value = 0

        for learningResourceType in learning_resource_types:
            if learningResourceType in learning_resource_type_possible_active_values:
                self.learning_style_active_value += 1

            if learningResourceType in learning_resource_type_possible_reflexive_values:
                self.learning_style_reflexive_value += 1

            if learningResourceType in learning_resource_type_possible_sensory_values:
                self.learning_style_sensory_value += 1

            if learningResourceType in learning_resource_type_possible_intuitive_values:
                self.learning_style_intuitive_value += 1

            if learningResourceType in learning_resource_type_possible_visual_values:
                self.learning_style_visual_value += 1

            if learningResourceType in learning_resource_type_possible_verbal_values:
                self.learning_style_verbal_value += 1

            if learningResourceType in learning_resource_type_possible_sequential_values:
                self.learning_style_sequential_value += 1

            if learningResourceType in learning_resource_type_possible_global_values:
                self.learning_style_global_value += 1

        if interativity_level == "very low":
            self.learning_style_active_value += 0
        elif interativity_level == "low":
            self.learning_style_active_value += 1
        elif interativity_level == "medium":
            self.learning_style_active_value += 2
        elif interativity_level == "high":
            self.learning_style_active_value += 3
        elif interativity_level == "very high":
            self.learning_style_active_value += 4
        else:
            print("Nível de interatividade não mapeado: {}".format(interativity_level))

        if interativity_type == "active":
            self.learning_style_active_value += 1
        elif interativity_type == "expositive":
            self.learning_style_reflexive_value += 1
        elif interativity_type == "mixed":
            self.learning_style_active_value += 1
            self.learning_style_reflexive_value += 1
        else:
            print("Tipo de interatividade não mapeado: {}".format(interativity_type))

        self.learning_resource_types = None
        self.interativity_level = ''
        self.interativity_type = ''
        self.covered_concepts = None

    def __str__(self):
        return "LearningMaterial{" + "id=" + str(self.id) + ", name=" + self.name + ", type=" + self.type + ", typical_learning_time=" + str(self.typical_learning_time) + ", dificulty=" + str(self.difficulty) + ", couveredConcepts=" + str(self.covered_concepts) + '}'
