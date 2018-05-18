import xml.etree.ElementTree as xml
import os
from courseconfig import CourseConfig
from concept import Concept
from learningmaterial import LearningMaterial
from learner import Learner


class Course:
    def __init__(self, configFile):
        courseConfig = CourseConfig(configFile)

        with open(courseConfig.conceptsFile, 'r') as br:
            self.concepts = {}
            for line in br:
                ccp_info = line.split('\n')[0].split(';')
                abbreviation = ccp_info[0]
                conceptName = ccp_info[1]
                self.concepts[abbreviation] = Concept(conceptName, abbreviation)

        lomFiles = os.listdir(courseConfig.learningMaterialsLOM)
        list.sort(lomFiles)

        self.learningMaterials = {}

        for lomFile in lomFiles:
            tree = xml.parse(lomFile)

            root = tree.getroot()

            pref = root.tag.split('}')[0] + '}'

            materialID = int(root.find('./' + pref + 'general/' + pref + 'identifier/' + pref + 'entry').text)
            materialName = root.find('./' + pref + 'general/' + pref + 'title/' + pref + 'string').text
            materialType = root.find('./' + pref + 'technical/' + pref + 'format').text
            typicalLearningTime = root.find('./' + pref + 'educational/' + pref + 'typicalLearningTime/' + pref + 'duration').text
            difficulty = root.find('./' + pref + 'educational/' + pref + 'difficulty/' + pref + 'value').text
            interactivityLevel = root.find('./' + pref + 'educational/' + pref + 'interactivityLevel/' + pref + 'value').text
            interactivityType = root.find('./' + pref + 'educational/' + pref + 'interactivityType/' + pref + 'value').text
            learningResourceType = []

            for i in root.findall('./' + pref + 'educational/' + pref + 'learningResourceType/' + pref + 'value'):
                learningResourceType.append(i.text)

            learningMaterial = LearningMaterial(materialID, materialName, materialType, typicalLearningTime, difficulty, learningResourceType, interactivityLevel, interactivityType)
            self.learningMaterials[materialID] = learningMaterial

            with open(courseConfig.learningMaterialsFile, 'r') as br:
                for line in br:
                    ccp_info = line.split('\n')[0].split(';')
                    learningMaterialID = int(ccp_info[0])
                    learningMaterial = self.learningMaterials[learningMaterialID]
                    for i in range(2, len(ccp_info)):
                        conceptAbbreviation = ccp_info[i]
                        conceptMaterial = self.concepts[conceptAbbreviation]

                        if learningMaterial.coveredConcepts is None:
                            learningMaterial.coveredConcepts = []
                        learningMaterial.coveredConcepts.append(conceptMaterial)

                        if conceptMaterial.LMs is None:
                            conceptMaterial.LMs = []
                        conceptMaterial.LMs.append(learningMaterial)

            with open(courseConfig.learnersFile, 'r') as br:
                self.learners = {}
                for line in br:
                    ccp_info = line.split('\n')[0].split(';')
                    if len(ccp_info) > 7:
                        learningGoals = []
                        for i in range(7, len(ccp_info)):
                            learnerLearningGoal = ccp_info[i]
                            learningGoals.append(self.concepts[learnerLearningGoal])

                        registrationCode = ccp_info[0]
                        learnerLowerTime = float(ccp_info[1])
                        learnerUpperTime = float(ccp_info[2])
                        atvref = int(ccp_info[3])
                        senint = int(ccp_info[4])
                        visver = int(ccp_info[5])
                        seqglo = int(ccp_info[6])

                        learner = Learner(registrationCode, learnerLowerTime, learnerUpperTime, atvref, senint, visver, seqglo, learningGoals)
                        self.learners[registrationCode] = learner

            with open(courseConfig.learnersScoreFile, 'r') as br:
                score = {}
                concept = None
                for line in br:
                    ccp_info = line.split('\n')[0].split(';')
                    learnerRegistrationCode = ccp_info[0]
                    conceptAbbreviation = ccp_info[1]
                    conceptScore = float(ccp_info[2])
                    learner = self.learners[learnerRegistrationCode]
                    concept = self.concepts[conceptAbbreviation]

                    if learner.score is None:
                        learner.score = {}
                    learner.score[concept] = conceptScore
