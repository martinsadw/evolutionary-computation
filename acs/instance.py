import numpy as np

from acs.course import Course


class Instance:
    def __init__(self):
        self.num_concepts = 0
        self.num_materials = 0

        self.student_abilities = None
        self.objectives = None

        self.duration_min = 0
        self.duration_max = 0
        self.student_active_reflexive = 0
        self.student_sensory_intuitive = 0
        self.student_visual_verbal = 0
        self.student_sequential_global = 0

        self.materials_difficulty = None
        self.concepts_materials = None
        self.estimated_time = None
        self.materials_active_reflexive = None
        self.materials_sensory_intuitive = None
        self.materials_visual_verbal = None
        self.materials_sequential_global = None

        self.missing_concepts_coeficient = 1

        self.concepts_covered_weight = 1
        self.difficulty_weight = 1
        self.total_time_weight = 1
        self.materials_balancing_weight = 1
        self.learning_style_weight = 1

    @classmethod
    def load_from_file(cls, config_filename):
        instance = cls()

        course = Course(config_filename)

        instance.concepts = course.concepts
        instance.materials = course.learning_materials
        instance.learners = course.learners

        instance.concepts_keys = [concept for concept in course.concepts]
        instance.materials_keys = [material for material in course.learning_materials]
        instance.learners_keys = [learner for learner in course.learners]

        instance.num_concepts = len(course.concepts)
        instance.num_materials = len(course.learning_materials)
        instance.num_learners = len(course.learners)

        # TODO(andre:2018-05-21): Garantir que a ordem das disciplinas está correta
        # TODO(andre:2018-05-21): Modificar o restante do codigo para aceitar
        # multiplos alunos e então modificar essas atribuições
        instance.student_abilities = np.empty((instance.num_learners, instance.num_concepts))
        for learner in range(instance.num_learners):
            for concept in range(instance.num_concepts):
                try:
                    instance.student_abilities[learner, concept] = course.learners[instance.learners_keys[learner]].score[instance.concepts_keys[concept]]
                except KeyError:
                    instance.student_abilities[learner, concept] = 0
        instance.student_abilities = instance.student_abilities[0]
        # instance.student_abilities = np.array([[course.learners[learner].score[score] for score in course.learners[learner].score] for learner in course.learners])

        instance.objectives = np.empty((instance.num_learners, instance.num_concepts), dtype=bool)
        for learner in range(instance.num_learners):
            for concept in range(instance.num_concepts):
                try:
                    if instance.concepts_keys[concept] in course.learners[instance.learners_keys[learner]].learning_goals:
                        instance.objectives[learner, concept] = True
                    else:
                        instance.objectives[learner, concept] = False
                except (KeyError, TypeError):
                    instance.objectives[learner, concept] = False
        instance.objectives = instance.objectives[0]
        # instance.objectives = np.array([course.learners[learner].learning_goals for learner in course.learners])
        # instance.objectives = instance.objectives[0]

        instance.duration_min = np.array([course.learners[learner].lower_time for learner in course.learners])
        instance.duration_min = instance.duration_min[0]

        instance.duration_max = np.array([course.learners[learner].upper_time for learner in course.learners])
        instance.duration_max = instance.duration_max[0]

        instance.student_active_reflexive = np.array([course.learners[learner].active_reflexive for learner in course.learners])
        instance.student_active_reflexive = instance.student_active_reflexive[0]

        instance.student_sensory_intuitive = np.array([course.learners[learner].sensory_intuitive for learner in course.learners])
        instance.student_sensory_intuitive = instance.student_sensory_intuitive[0]

        instance.student_visual_verbal = np.array([course.learners[learner].visual_verbal for learner in course.learners])
        instance.student_visual_verbal = instance.student_visual_verbal[0]

        instance.student_sequential_global = np.array([course.learners[learner].sequential_global for learner in course.learners])
        instance.student_sequential_global = instance.student_sequential_global[0]

        instance.materials_difficulty = np.array([course.learning_materials[material].difficulty for material in course.learning_materials])

        instance.concepts_materials = np.zeros((instance.num_concepts, instance.num_materials), dtype=bool)
        for material in range(instance.num_materials):
            for concept in range(instance.num_concepts):
                if instance.concepts_keys[concept] in course.material_coverage[instance.materials_keys[material]]:
                    instance.concepts_materials[concept, material] = True
        # instance.concepts_materials = np.array([course.concepts[concept].learning_materials for concept in course.concepts])

        instance.estimated_time = np.array([course.learning_materials[material].typical_learning_time for material in course.learning_materials])

        instance.materials_active_reflexive = np.array([course.learning_materials[material].active_reflexive for material in course.learning_materials])
        instance.materials_sensory_intuitive = np.array([course.learning_materials[material].sensory_intuitive for material in course.learning_materials])
        instance.materials_visual_verbal = np.array([course.learning_materials[material].visual_verbal for material in course.learning_materials])
        instance.materials_sequential_global = np.array([course.learning_materials[material].sequential_global for material in course.learning_materials])

        instance.missing_concepts_coeficient = course.missing_concepts_coeficient
        instance.concepts_covered_weight = course.concepts_covered_weight
        instance.difficulty_weight = course.difficulty_weight
        instance.total_time_weight = course.total_time_weight
        instance.materials_balancing_weight = course.materials_balancing_weight
        instance.learning_style_weight = course.learning_style_weight

        return instance

    @classmethod
    def load_test(cls):
        instance = cls()

        concepts_description = [0, 0, 0, 0, 0]
        materials_description = [0, 0, 0, 0, 0, 0, 0]
        # instance['materials_description'] = np.array([1, 0, 1, 0, 1, 0, 0], dtype=bool)

        instance.num_concepts = len(concepts_description)
        instance.num_materials = len(materials_description)

        instance.student_abilities = np.array([0.5, 0.3, 0.1, 0.2, 0.9])
        instance.objectives = np.array([0, 1, 1, 1, 0], dtype=bool)

        instance.duration_min = 0
        instance.duration_max = 50
        instance.student_active_reflexive = 3
        instance.student_sensory_intuitive = 2
        instance.student_visual_verbal = -1
        instance.student_sequential_global = -2

        instance.materials_difficulty = np.array([0.8, 0.7, 0.8, 0.3, 0.5, 0.1, 0.3])
        instance.concepts_materials = np.array([
            [0, 0, 0, 0, 1, 1, 0],
            [1, 0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 1],
        ], dtype=bool)
        instance.estimated_time = np.array([20, 20, 30, 45, 10, 50, 35])
        instance.materials_active_reflexive = np.array([2, 1, -2, -4, 3, 0, -1])
        instance.materials_sensory_intuitive = np.array([1, 4, 3, -2, -3, 0, 2])
        instance.materials_visual_verbal = np.array([2, -1, -1, 5, 0, 0, 3])
        instance.materials_sequential_global = np.array([-3, -2, 2, 1, 3, 3, -1])

        instance.missing_concepts_coeficient = 2

        instance.concepts_covered_weight = 1
        instance.difficulty_weight = 1
        instance.total_time_weight = 1
        instance.materials_balancing_weight = 1
        instance.learning_style_weight = 1

        return instance


def print_instance(instance):
    print("Cobertura dos materiais:")
    print(instance.concepts_materials)

    print("\nObjetivos do aluno:")
    print(instance.objectives)

    print("\nHabilidades do aluno:")
    print(instance.student_abilities)

    print("\nDificuldades dos materiais:")
    print(instance.materials_difficulty)

    print("\nDuração dos materiais:")
    print(instance.estimated_time)

    print("\nDuração mínima:")
    print(instance.duration_min)

    print("\nDuração máxima:")
    print(instance.duration_max)

    print("\nEstilo dos materiais:")
    print("     Ativo | Reflexivo: {}".format(instance.materials_active_reflexive))
    print(" Sensorial | Intuitivo: {}".format(instance.materials_sensory_intuitive))
    print("    Visual | Verbal:    {}".format(instance.materials_visual_verbal))
    print("Sequencial | Global:    {}".format(instance.materials_sequential_global))

    print("\nEstilo do aluno:")
    print("     Ativo | Reflexivo: {}".format(instance.student_active_reflexive))
    print(" Sensorial | Intuitivo: {}".format(instance.student_sensory_intuitive))
    print("    Visual | Verbal:    {}".format(instance.student_visual_verbal))
    print("Sequencial | Global:    {}".format(instance.student_sequential_global))
