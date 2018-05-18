import configparser


class CourseConfig:
    def __init__(self, configFile):
        configString = '[section]\n'  # python precisa de um "section" para ler o arquivo de configurações
        with open(configFile, 'r') as file:
            configString += file.read()

        config = configparser.ConfigParser()
        config.read_string(configString)

        self.__path = config['section']['ppatosca.path']
        self.learningMaterialsLOM = config['section']['ppatosca.path.learningMaterialsLOM']

        self.conceptsFile = self.__path + config['section']['ppatosca.file.concepts']
        self.prerequisitesFile = self.__path + config['section']['ppatosca.file.prerequisites']
        self.learningMaterialsFile = self.__path + config['section']['ppatosca.file.learningMaterials']
        self.learnersFile = self.__path + config['section']['ppatosca.file.learners']
        self.learnersScoreFile = self.__path + config['section']['ppatosca.file.learnersScore']
