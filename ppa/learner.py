class Learner:
    # TODO(andre:2018-05-19): Permitir criar um instancia de Learner passando
    # uma string com o nome do arquivo com as informacoes do estudante
    def __init__(self, registration_code, lower_time, upper_time, active_reflexive, sensory_intuitive, visual_verbal, sequential_global, learning_goals):
        self.id = 0
        self.score = None
        self.active_reflexive = 0
        self.sensory_intuitive = 0
        self.visual_verbal = 0
        self.sequential_global = 0

        self.registration_code = registration_code
        self.lower_time = int(lower_time * 3600)
        self.upper_time = int(upper_time * 3600)

        self.learning_goals = learning_goals

        if active_reflexive == -11 or active_reflexive == -9:
            self.active_reflexive = -3
        elif active_reflexive == -7 or active_reflexive == -5:
            self.active_reflexive = -2
        elif active_reflexive == -3 or active_reflexive == -1:
            self.active_reflexive = -1
        elif active_reflexive == 11 or active_reflexive == 9:
            self.active_reflexive = 3
        elif active_reflexive == 7 or active_reflexive == 5:
            self.active_reflexive = 2
        elif active_reflexive == 3 or active_reflexive == 1:
            self.active_reflexive = 1

        if sensory_intuitive == -11 or sensory_intuitive == -9:
            self.sensory_intuitive = -3
        elif sensory_intuitive == -7 or sensory_intuitive == -5:
            self.sensory_intuitive = -2
        elif sensory_intuitive == -3 or sensory_intuitive == -1:
            self.sensory_intuitive = -1
        elif sensory_intuitive == 11 or sensory_intuitive == 9:
            self.sensory_intuitive = 3
        elif sensory_intuitive == 7 or sensory_intuitive == 5:
            self.sensory_intuitive = 2
        elif sensory_intuitive == 3 or sensory_intuitive == 1:
            self.sensory_intuitive = 1

        if visual_verbal == -11 or visual_verbal == -9:
            self.visual_verbal = -3
        elif visual_verbal == -7 or visual_verbal == -5:
            self.visual_verbal = -2
        elif visual_verbal == -3 or visual_verbal == -1:
            self.visual_verbal = -1
        elif visual_verbal == 11 or visual_verbal == 9:
            self.visual_verbal = 3
        elif visual_verbal == 7 or visual_verbal == 5:
            self.visual_verbal = 2
        elif visual_verbal == 3 or visual_verbal == 1:
            self.visual_verbal = 1

        if sequential_global == -11 or sequential_global == -9:
            self.sequential_global = -3
        elif sequential_global == -7 or sequential_global == -5:
            self.sequential_global = -2
        elif sequential_global == -3 or sequential_global == -1:
            self.sequential_global = -1
        elif sequential_global == 11 or sequential_global == 9:
            self.sequential_global = 3
        elif sequential_global == 7 or sequential_global == 5:
            self.sequential_global = 2
        elif sequential_global == 3 or sequential_global == 1:
            self.sequential_global = 1

    def __str__(self):
        score_str = ""
        for concept in self.score:
            score_str += concept.abbreviation + "=" + str(self.score[concept]) + ", "
        score_str = score_str[:-2]

        return "Learner{id=" + str(self.id) + ", score={" + score_str + "}, active_reflexive=" + str(self.active_reflexive) + ", sensory_intuitive=" + str(self.sensory_intuitive) + ", visual_verbal=" + str(self.visual_verbal) + ", sequential_global=" + str(self.sequential_global) + ", registration_code=" + str(self.registration_code) + ", lower_time=" + str(self.lower_time) + ", upper_time=" + str(self.upper_time) + "}"
