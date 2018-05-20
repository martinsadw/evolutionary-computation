import xml.etree.ElementTree as xml
import os
from course_config import CourseConfig
from concept import Concept
from learning_material import LearningMaterial
from learner import Learner


class Course:
    def __init__(self, config_filename):
        course_config = CourseConfig(config_filename)

        self.concepts = {}
        with open(course_config.concepts_filename, 'r') as concepts_file:
            for line in concepts_file:
                ccp_info = line.split('\n')[0].split(';')
                abbreviation = ccp_info[0]
                concept_name = ccp_info[1]
                self.concepts[abbreviation] = Concept(concept_name, abbreviation)

        self.learning_materials = {}

        # TODO(andre:2018-05-19): Mover procedimento de leitura de arquivo LOM
        # para dentro da classe LearningMaterial
        for root, dirs, files in os.walk(course_config.learning_materials_lom):
            for lom_file in files:
                if lom_file.endswith('.xml'):
                    tree = xml.parse(os.path.join(root, lom_file))

                    xml_root = tree.getroot()

                    pref = xml_root.tag.split('}')[0] + '}'

                    material_id = int(xml_root.find('./' + pref + 'general/' + pref + 'identifier/' + pref + 'entry').text)
                    material_name = xml_root.find('./' + pref + 'general/' + pref + 'title/' + pref + 'string').text
                    material_type = xml_root.find('./' + pref + 'technical/' + pref + 'format').text
                    typical_learning_time = xml_root.find('./' + pref + 'educational/' + pref + 'typicalLearningTime/' + pref + 'duration').text
                    difficulty = xml_root.find('./' + pref + 'educational/' + pref + 'difficulty/' + pref + 'value').text
                    interactivity_level = xml_root.find('./' + pref + 'educational/' + pref + 'interactivityLevel/' + pref + 'value').text
                    interactivity_type = xml_root.find('./' + pref + 'educational/' + pref + 'interactivityType/' + pref + 'value').text
                    learning_resource_type = []

                    for i in xml_root.findall('./' + pref + 'educational/' + pref + 'learningResourceType/' + pref + 'value'):
                        learning_resource_type.append(i.text)

                    learning_material = LearningMaterial(material_id, material_name, material_type, typical_learning_time, difficulty, learning_resource_type, interactivity_level, interactivity_type)
                    self.learning_materials[material_id] = learning_material

        with open(course_config.learning_materials_filename, 'r') as learning_materials_file:
            for line in learning_materials_file:
                ccp_info = line.split('\n')[0].split(';')
                learning_material_id = int(ccp_info[0])
                learning_material = self.learning_materials[learning_material_id]
                for i in range(2, len(ccp_info)):
                    concept_abbreviation = ccp_info[i]
                    concept_material = self.concepts[concept_abbreviation]

                    if learning_material.covered_concepts is None:
                        learning_material.covered_concepts = []
                    learning_material.covered_concepts.append(concept_material)

                    if concept_material.learning_materials is None:
                        concept_material.learning_materials = []
                    concept_material.learning_materials.append(learning_material)

        self.learners = {}
        with open(course_config.learners_filename, 'r') as learners_file:
            for line in learners_file:
                ccp_info = line.split('\n')[0].split(';')
                if len(ccp_info) > 7:
                    learning_goals = []
                    for i in range(7, len(ccp_info)):
                        learner_learning_goal = ccp_info[i]
                        learning_goals.append(self.concepts[learner_learning_goal])

                    registration_code = ccp_info[0]
                    learner_lower_time = float(ccp_info[1])
                    learner_upper_time = float(ccp_info[2])
                    active_reflexive = int(ccp_info[3])
                    sensory_intuitive = int(ccp_info[4])
                    visual_verbal = int(ccp_info[5])
                    sequential_global = int(ccp_info[6])

                    learner = Learner(registration_code, learner_lower_time, learner_upper_time, active_reflexive, sensory_intuitive, visual_verbal, sequential_global, learning_goals)
                    self.learners[registration_code] = learner

        with open(course_config.learners_score_filename, 'r') as learners_score_file:
            concept = None
            for line in learners_score_file:
                ccp_info = line.split('\n')[0].split(';')
                learner_registration_code = ccp_info[0]
                concept_abbreviation = ccp_info[1]
                concept_score = float(ccp_info[2])
                learner = self.learners[learner_registration_code]
                concept = self.concepts[concept_abbreviation]

                if learner.score is None:
                    learner.score = {}
                learner.score[concept] = concept_score


if __name__ == "__main__":
    course = Course("../instance_files/config.txt")

    for material in course.learning_materials:
        print(str(course.learning_materials[material]))

    for concept in course.concepts:
        print(str(course.concepts[concept]))

    for learner in course.learners:
        print(str(course.learners[learner]))
