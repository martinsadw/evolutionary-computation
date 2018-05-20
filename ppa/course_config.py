import configparser
import os


class CourseConfig:
    def __init__(self, config_filename):
        config_string = '[section]\n'  # python precisa de um "section" para ler o arquivo de configurações
        with open(config_filename, 'r') as file:
            config_string += file.read()

        config = configparser.ConfigParser()
        config.read_string(config_string)

        self.__path = config['section']['ppatosca.path']
        self.learning_materials_lom = os.path.join(self.__path, config['section']['ppatosca.path.learningMaterialsLOM'])

        self.concepts_filename = os.path.join(self.__path, config['section']['ppatosca.file.concepts'])
        self.prerequisites_filename = os.path.join(self.__path, config['section']['ppatosca.file.prerequisites'])
        self.learning_materials_filename = os.path.join(self.__path, config['section']['ppatosca.file.learningMaterials'])
        self.learners_filename = os.path.join(self.__path, config['section']['ppatosca.file.learners'])
        self.learners_score_filename = os.path.join(self.__path, config['section']['ppatosca.file.learnersScore'])
