import xml.etree.ElementTree as xml
import configparser
import os
from concept import Concept
from learning_material import LearningMaterial
from learner import Learner
from collections import defaultdict


class Course:
    def __init__(self, config_filename):
        # config_string = '[section]\n'  # python precisa de um "section" para ler o arquivo de configurações
        with open(config_filename, 'r') as config_file:
            config_string = config_file.read()
        config = configparser.ConfigParser()
        config.read_string(config_string)

        dirname = os.path.dirname(config_filename)
        path = config['section']['ppatosca.path']
        learning_materials_lom      = os.path.normpath(os.path.join(dirname, path, config['section']['ppatosca.path.learningMaterialsLOM']))
        concepts_filename           = os.path.normpath(os.path.join(dirname, path, config['section']['ppatosca.file.concepts']))
        material_coverage_filename  = os.path.normpath(os.path.join(dirname, path, config['section']['ppatosca.file.materialsCoverage']))
        learners_filename           = os.path.normpath(os.path.join(dirname, path, config['section']['ppatosca.file.learners']))
        learners_score_filename     = os.path.normpath(os.path.join(dirname, path, config['section']['ppatosca.file.learnersScore']))
        fitness_parameters_filename = os.path.normpath(os.path.join(dirname, path, config['section']['ppatosca.file.fitnessParameters']))
        # prerequisites_filename      = os.path.normpath(os.path.join(dirname, path, config['section']['ppatosca.file.prerequisites']))

        self.concepts = {}
        with open(concepts_filename, 'r') as concepts_file:
            for line in concepts_file:
                # A leitura de arquivos do python converte os caracteres de fim de linha em \n
                concept = Concept.load_from_string(line.rstrip('\n'))
                self.concepts[concept.abbreviation] = concept

        self.learning_materials = {}
        for root, dirs, files in os.walk(learning_materials_lom):
            for lom_file in files:
                if lom_file.endswith('.xml'):
                    learning_material = LearningMaterial.load_from_file(os.path.join(root, lom_file))
                    self.learning_materials[learning_material.id] = learning_material

        # TODO(andre:2018-06-15): Oferecer opção 'strict' para retornar erro
        # caso o curso ou o material nesse arquivo não existam
        self.material_coverage = defaultdict(set)
        with open(material_coverage_filename, 'r') as material_coverage_file:
            for line in material_coverage_file:
                material_fields = line.rstrip('\n').split(';')

                material_id = int(material_fields[0])
                self.material_coverage[material_id].update(material_fields[2:])

        self.learners = {}
        with open(learners_filename, 'r') as learners_file:
            for line in learners_file:
                # A leitura de arquivos do python converte os caracteres de fim de linha em \n
                learner = Learner.load_from_string(line.rstrip('\n'))
                self.learners[learner.id] = learner

        # TODO(andre:2018-06-15): Oferecer opção 'strict' para retornar erro
        # caso o aluno nesse arquivo não exista
        with open(learners_score_filename, 'r') as learners_score_file:
            for line in learners_score_file:
                score_fields = line.rstrip('\n').split(';')

                learner_id = score_fields[0]
                concept_abbreviation = score_fields[1]
                concept_score = float(score_fields[2])

                if learner_id in self.learners:
                    self.learners[learner_id].score[concept_abbreviation] = concept_score

        with open(fitness_parameters_filename, 'r') as fitness_parameters_file:
            fitness_string = fitness_parameters_file.read()
            config = configparser.ConfigParser(inline_comment_prefixes=(';',))
            config.read_string(fitness_string)

            self.missing_concepts_coeficient = float(config['section']['ppatosca.fitness.missingConceptsCoeficient'])
            self.concepts_covered_weight = float(config['section']['ppatosca.fitness.conceptsCoveredWeight'])
            self.difficulty_weight = float(config['section']['ppatosca.fitness.difficultyWeight'])
            self.total_time_weight = float(config['section']['ppatosca.fitness.totalTimeWeight'])
            self.materials_balancing_weight = float(config['section']['ppatosca.fitness.materialsBalancingWeight'])
            self.learning_style_weight = float(config['section']['ppatosca.fitness.learningStyleWeight'])


if __name__ == "__main__":
    course = Course("../instances/test/instance_config.txt")

    for material in course.learning_materials:
        print(str(course.learning_materials[material]))

    for concept in course.concepts:
        print(str(course.concepts[concept]))

    for learner in course.learners:
        print(str(course.learners[learner]))
