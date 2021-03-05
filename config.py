import os

from acs.instance import Instance
from read.algorithm import open_results

dir = os.path.dirname(__file__)

instance = Instance.load_from_file(os.path.join(dir,'instances','real', 'instance.txt'))

concept_coverage = instance.concepts_materials.T
objectives = instance.objectives

_acs_results = open_results('2020-01-16_real_5_100000.pickle')
_algorithm = 'de'
_repetition = 0
recommendation = _acs_results[_algorithm][0][_repetition].T # 284x24

num_materials = concept_coverage.shape[0]
num_concepts = concept_coverage.shape[1]
num_students = recommendation.shape[1]