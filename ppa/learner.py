_map_axis_values = {
    -11: -3,
    -9: -3,
    -7: -2,
    -5: -2,
    -3: -1,
    -1: -1,
    1: 1,
    3: 1,
    5: 2,
    7: 2,
    9: 3,
    11: 3,
}

class Learner:
    def __init__(self, id, lower_time, upper_time, active_reflexive, sensory_intuitive, visual_verbal, sequential_global, learning_goals):
        self.score = {}

        self.id = id
        self.lower_time = int(lower_time * 3600)
        self.upper_time = int(upper_time * 3600)

        self.learning_goals = learning_goals

        assert(active_reflexive in _map_axis_values)
        assert(sensory_intuitive in _map_axis_values)
        assert(visual_verbal in _map_axis_values)
        assert(sequential_global in _map_axis_values)

        self.active_reflexive = _map_axis_values[active_reflexive]
        self.sensory_intuitive = _map_axis_values[sensory_intuitive]
        self.visual_verbal = _map_axis_values[visual_verbal]
        self.sequential_global = _map_axis_values[sequential_global]

    @classmethod
    def load_from_string(cls, description):
        fields = description.split(';')
        assert(len(fields) > 7)

        id = fields[0]
        learner_lower_time = float(fields[1])
        learner_upper_time = float(fields[2])
        active_reflexive = int(fields[3])
        sensory_intuitive = int(fields[4])
        visual_verbal = int(fields[5])
        sequential_global = int(fields[6])
        learning_goals = set(fields[7:])

        return cls(id, learner_lower_time, learner_upper_time, active_reflexive, sensory_intuitive, visual_verbal, sequential_global, learning_goals)

    def __str__(self):
        score_str = ""
        for concept in self.score:
            score_str += concept + "=" + str(self.score[concept]) + ", "
        score_str = score_str[:-2]

        return "Learner{id=" + str(self.id) + ", score={" + score_str + "}, active_reflexive=" + str(self.active_reflexive) + ", sensory_intuitive=" + str(self.sensory_intuitive) + ", visual_verbal=" + str(self.visual_verbal) + ", sequential_global=" + str(self.sequential_global) + ", lower_time=" + str(self.lower_time) + ", upper_time=" + str(self.upper_time) + "}"
