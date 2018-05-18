class LearningMaterial:
    def __init__(self, paramId, name, paramType, typicalLearningTime, difficulty, learningResourceTypes, interativityLevel, interativityType):
        learningResourceTypePossibleActiveValues = ['exercise', 'simulation', 'questionnaire', 'test', 'experiment']
        learningResourceTypePossibleReflexiveValues = ['simulation', 'diagram', 'figure', 'graphic', 'slide', 'table', 'narrative text', 'test', 'problems declaration']

        learningResourceTypePossibleSensoryValues = ["exercise", "simulation", "graphic", "slide", "test", "table", "narrative text", "experiment", "problems declaration"]
        learningResourceTypePossibleIntuitiveValues = ["simulation", "questionnaire", "diagram", "test", "figure", "slide", "narrative text"]

        learningResourceTypePossibleVisualValues = ["simulation", "diagram", "figure", "graphic", "slide", "table"]
        learningResourceTypePossibleVerbalValues = ["slide", "narrative text", "reading"]

        learningResourceTypePossibleSequentialValues = ["exercise", "simulation", "diagram", "slide", "narrative text", "experiment"]
        learningResourceTypePossibleGlobalValues = ["diagram", "figure", "graphic", "slide", "table", "narrative text"]

        hour = 0
        minute = 0
        second = 0
        self.id = paramId
        self.name = name
        self.type = paramType

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
            print("Dificuldade não mapeada: " + difficulty)
            self.difficulty = 0.0

        typicalLearningTime = typicalLearningTime.replace("PT", "")
        if "H" in typicalLearningTime:
            hour = int(typicalLearningTime.split("H")[0])
            if len(typicalLearningTime.split("H")) == 2:
                typicalLearningTime = typicalLearningTime.split("H")[1]

        if "M" in typicalLearningTime:
            minute = int(typicalLearningTime.split("M")[0])
            if len(typicalLearningTime.split("M")) == 2:
                typicalLearningTime = typicalLearningTime.split("M")[1]

        if "S" in typicalLearningTime:
            second = int(typicalLearningTime.replace("S", "")[0])

        self.typicalLearningTime = (hour * 3600) + (minute * 60) + second

        self.learningStyleActiveValue = 0
        self.learningStyleReflexiveValue = 0
        self.learningStyleSensoryValue = 0
        self.learningStyleIntuitiveValue = 0
        self.learningStyleVisualValue = 0
        self.learningStyleVerbalValue = 0
        self.learningStyleSequentialValue = 0
        self.learningStyleGlobalValue = 0

        for learningResourceType in learningResourceTypes:
            if learningResourceType in learningResourceTypePossibleActiveValues:
                self.learningStyleActiveValue += 1

            if learningResourceType in learningResourceTypePossibleReflexiveValues:
                self.learningStyleReflexiveValue += 1

            if learningResourceType in learningResourceTypePossibleSensoryValues:
                self.learningStyleSensoryValue += 1

            if learningResourceType in learningResourceTypePossibleIntuitiveValues:
                self.learningStyleIntuitiveValue += 1

            if learningResourceType in learningResourceTypePossibleVisualValues:
                self.learningStyleVisualValue += 1

            if learningResourceType in learningResourceTypePossibleVerbalValues:
                self.learningStyleVerbalValue += 1

            if learningResourceType in learningResourceTypePossibleSequentialValues:
                self.learningStyleSequentialValue += 1

            if learningResourceType in learningResourceTypePossibleGlobalValues:
                self.learningStyleGlobalValue += 1

        if interativityLevel == "low":
            self.learningStyleActiveValue += 1
        elif interativityLevel == "medium":
            self.learningStyleActiveValue += 2
        elif interativityLevel == "high":
            self.learningStyleActiveValue += 3
        elif interativityLevel == "very high":
            self.learningStyleActiveValue += 4
        else:
            print("nivel de interatividade não mapeado: " + interativityLevel)

        if interativityType == "active":
            self.learningStyleActiveValue += 1
        elif interativityType == "expositive":
            self.learningStyleReflexiveValue += 1
        elif interativityType == "mixed":
            self.learningStyleActiveValue += 1
            self.learningStyleReflexiveValue += 1
        else:
            print("Tipo de interatividade não mapeado: "+interativityType)

        self.learningResourceTypes = None
        self.interativityLevel = ''
        self.interativityType = ''
        self.coveredConcepts = None

    def __str__(self):
        return "LearningMaterial{" + "id=" + self.id + ", name=" + self.name + ", type=" + self.type + ", typical_learning_time=" + self.typicalLearningTime + ", dificulty=" + self.difficulty + ", couveredConcepts=" + self.coveredConcepts + '}'
