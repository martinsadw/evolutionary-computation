import configparser
import csv
import math
import os


def write_parameters_file(filename):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.add_section('section')

    config['section']['acs.fitness.missingConceptsCoeficient'] = '2'
    config['section']['acs.fitness.conceptsCoveredWeight'] = '1'
    config['section']['acs.fitness.difficultyWeight'] = '1'
    config['section']['acs.fitness.totalTimeWeight'] = '0.00166666666666666666666666666667'
    config['section']['acs.fitness.materialsBalancingWeight'] = '1'
    config['section']['acs.fitness.learningStyleWeight'] = '1'

    with open(filename, 'w') as parameters_file:
        config.write(parameters_file)


def write_learners_file(learner_filename, scores_filename, stats, sort=True):
    learners = stats['instance'].learners.items()
    if sort:
        learners = sorted(learners)

    with open(learner_filename, 'w') as learners_file:
        learners_writer = csv.writer(learners_file, delimiter=';')

        for id, learner in learners:
            lower_time = learner.lower_time // 3600
            upper_time = learner.upper_time // 3600

            active_reflexive  = learner.active_reflexive  * 4 - int(math.copysign(1, learner.active_reflexive))
            sensory_intuitive = learner.sensory_intuitive * 4 - int(math.copysign(1, learner.sensory_intuitive))
            visual_verbal     = learner.visual_verbal     * 4 - int(math.copysign(1, learner.visual_verbal))
            sequential_global = learner.sequential_global * 4 - int(math.copysign(1, learner.sequential_global))

            goals = sorted(learner.learning_goals)

            learners_writer.writerow([id, lower_time, upper_time, active_reflexive, sensory_intuitive, visual_verbal, sequential_global] + goals)

    with open(scores_filename, 'w') as scores_file:
        scores_writer = csv.writer(scores_file, delimiter=';')

        for id, learner in learners:
            scores = learner.score.items()
            if sort:
                scores = sorted(scores)

            for concept, score in scores:
                scores_writer.writerow([id, concept, score])


def write_concepts_file(filename, stats, sort=True):
    concepts = stats['instance'].concepts.items()
    if sort:
        concepts = sorted(concepts)

    with open(filename, 'w') as concepts_file:
        concepts_writer = csv.writer(concepts_file, delimiter=';')

        for abbreviation, concept in concepts:
            concepts_writer.writerow([abbreviation, concept.name])


def write_instance_file(path, stats,
                        instance_name='instance.txt',
                        parameters_name='parameters.txt',
                        concepts_name='concepts.csv',
                        learners_name='learners.csv',
                        score_name='learners_score.csv',
                        coverage_name='material_coverage.csv',
                        lom_name='LOM'):
    write_parameters_file(os.path.join(path, parameters_name))
    write_learners_file(os.path.join(path, learners_name), os.path.join(path, score_name), stats)
    write_concepts_file(os.path.join(path, concepts_name), stats)

    config = configparser.ConfigParser()
    config.optionxform = str
    config.add_section('section')

    config['section']['acs.path'] = '.'
    config['section']['acs.path.learningMaterialsLOM'] = lom_name

    config['section']['acs.file.concepts'] = concepts_name
    config['section']['acs.file.materialsCoverage'] = coverage_name
    config['section']['acs.file.learners'] = learners_name
    config['section']['acs.file.learnersScore'] = score_name
    config['section']['acs.file.fitnessParameters'] = parameters_name

    with open(os.path.join(path, instance_name), 'w') as instance_file:
        config.write(instance_file)
