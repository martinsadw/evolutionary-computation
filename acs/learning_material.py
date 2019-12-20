import re
import xml.etree.ElementTree as xml


_active_resource_types = set(['exercise', 'simulation', 'questionnaire', 'test', 'experiment'])
_reflexive_resource_types = set(['simulation', 'diagram', 'figure', 'graphic', 'slide', 'table', 'narrative text', 'test', 'problems declaration'])

_sensory_resource_types = set(["exercise", "simulation", "graphic", "slide", "test", "table", "narrative text", "experiment", "problems declaration"])
_intuitive_resource_types = set(["simulation", "questionnaire", "diagram", "test", "figure", "slide", "narrative text"])

_visual_resource_types = set(["simulation", "diagram", "figure", "graphic", "slide", "table"])
_verbal_resource_types = set(["slide", "narrative text", "reading"])

_sequential_resource_types = set(["exercise", "simulation", "diagram", "slide", "narrative text", "experiment"])
_global_resource_types = set(["diagram", "figure", "graphic", "slide", "table", "narrative text"])

_interactivity_level_active_values = {
    "very high": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
    "very low": 0
}

_difficulties = {
    "very difficult": 5,
    "difficult": 4,
    "medium": 3,
    "easy": 2,
    "very easy": 1
}

_interactivity_type_active_values = {
    "active": 1,
    "expositive": 0,
    "mixed": 1
}
_interactivity_type_reflexive_values = {
    "active": 0,
    "expositive": 1,
    "mixed": 1
}

class LearningMaterial:
    def __init__(self, id, name, type, typical_learning_time, difficulty, learning_resource_types, interactivity_level, interactivity_type):
        self.id = id
        self.name = name
        self.type = type

        if difficulty in _difficulties:
            self.difficulty = _difficulties[difficulty]
        else:
            print("Dificuldade não mapeada: {}".format(difficulty))
            self.difficulty = 0

        # TODO(andre:2018-07-20): Confirmar o formato das datas
        # time_regex = re.search(r"PT(?:(?P<hours>[0-9]+)H)?(?:(?P<minutes>[0-5]?[0-9]|60)M)?(?:(?P<seconds>[0-5]?[0-9]|60)S)?", typical_learning_time)
        time_regex = re.search(r"PT(?:(?P<hours>[0-9]+)H)?(?:(?P<minutes>[0-9]+)M)?(?:(?P<seconds>[0-5]?[0-9]|60)S)?", typical_learning_time)
        self.typical_learning_time = 0
        if time_regex.group('hours') is not None:
            self.typical_learning_time += int(time_regex.group('hours')) * 3600
        if time_regex.group('minutes') is not None:
            self.typical_learning_time += int(time_regex.group('minutes')) * 60
        if time_regex.group('seconds') is not None:
            self.typical_learning_time += int(time_regex.group('seconds'))

        self.learning_style_active_value = 0
        self.learning_style_reflexive_value = 0
        self.learning_style_sensory_value = 0
        self.learning_style_intuitive_value = 0
        self.learning_style_visual_value = 0
        self.learning_style_verbal_value = 0
        self.learning_style_sequential_value = 0
        self.learning_style_global_value = 0

        for learningResourceType in learning_resource_types:
            if learningResourceType in _active_resource_types:
                self.learning_style_active_value += 1

            if learningResourceType in _reflexive_resource_types:
                self.learning_style_reflexive_value += 1

            if learningResourceType in _sensory_resource_types:
                self.learning_style_sensory_value += 1

            if learningResourceType in _intuitive_resource_types:
                self.learning_style_intuitive_value += 1

            if learningResourceType in _visual_resource_types:
                self.learning_style_visual_value += 1

            if learningResourceType in _verbal_resource_types:
                self.learning_style_verbal_value += 1

            if learningResourceType in _sequential_resource_types:
                self.learning_style_sequential_value += 1

            if learningResourceType in _global_resource_types:
                self.learning_style_global_value += 1

        if interactivity_level in _interactivity_level_active_values:
            self.learning_style_active_value += _interactivity_level_active_values[interactivity_level]
        else:
            print("Nível de interatividade não mapeado: {}".format(interactivity_level))

        if interactivity_type in _interactivity_type_active_values:
            self.learning_style_active_value += _interactivity_type_active_values[interactivity_type]
            self.learning_style_reflexive_value += _interactivity_type_reflexive_values[interactivity_type]
        else:
            print("Tipo de interatividade não mapeado: {}".format(interactivity_type))

        self.active_reflexive = self.learning_style_active_value - self.learning_style_reflexive_value
        self.sensory_intuitive = self.learning_style_sensory_value - self.learning_style_intuitive_value
        self.visual_verbal = self.learning_style_visual_value - self.learning_style_verbal_value
        self.sequential_global = self.learning_style_sequential_value - self.learning_style_global_value

        self.learning_resource_types = learning_resource_types
        self.interactivity_level = interactivity_level
        self.interactivity_type = interactivity_type
        self.covered_concepts = None

    @classmethod
    def load_from_file(cls, filename):
        tree = xml.parse(filename)
        xml_root = tree.getroot()
        pref = xml_root.tag.split('}')[0] + '}'
        # print(xml_root)
        # xml.dump(xml_root)

        # TODO(andre:2018-06-15): Medida provisória. Remover isso depois que os arquivos de LOM for arrumado
        material_id = int(xml_root.find('./' + pref + 'general/' + pref + 'identifier/' + pref + 'entry').text)
        # material_name = xml_root.find('./' + pref + 'general/' + pref + 'title/' + pref + 'string').text
        material_name = "a"

        # material_id = int(xml_root.find('./' + pref + 'entry').text)
        # material_name = xml_root.find('./' + pref + 'title/' + pref + 'string').text

        material_type = xml_root.find('./' + pref + 'technical/' + pref + 'format').text
        typical_learning_time = xml_root.find('./' + pref + 'educational/' + pref + 'typicalLearningTime/' + pref + 'duration').text
        difficulty = xml_root.find('./' + pref + 'educational/' + pref + 'difficulty/' + pref + 'value').text
        interactivity_level = xml_root.find('./' + pref + 'educational/' + pref + 'interactivityLevel/' + pref + 'value').text
        interactivity_type = xml_root.find('./' + pref + 'educational/' + pref + 'interactivityType/' + pref + 'value').text

        learning_resource_type = []
        for type in xml_root.findall('./' + pref + 'educational/' + pref + 'learningResourceType/' + pref + 'value'):
            learning_resource_type.append(type.text)

        return cls(material_id, material_name, material_type, typical_learning_time, difficulty, learning_resource_type, interactivity_level, interactivity_type)

    def __str__(self):
        return "LearningMaterial{{id={}, typical_learning_time={}, difficulty={}, style=({}, {}, {}, {})}}".format(self.id, self.typical_learning_time, self.difficulty, self.active_reflexive, self.sensory_intuitive, self.visual_verbal, self.sequential_global)
        # return "LearningMaterial{" + "id=" + str(self.id) + ", name=" + self.name + ", type=" + self.type + ", typical_learning_time=" + str(self.typical_learning_time) + ", dificulty=" + str(self.difficulty) + ", coveredConcepts=" + str(self.covered_concepts) + '}'
