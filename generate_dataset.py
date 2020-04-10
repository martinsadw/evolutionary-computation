import argparse
import os
import pickle
import sys

from stats.extract import extract_data

from generator.main import generate_materials
from generator.concepts_selector import write_material_coverage_file
from generator.lom import write_lom_file
from generator.extra import write_instance_file

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('characteristics_file')

    parser.add_argument('-n', '--number-materials', type=int, default=1000)
    parser.add_argument('-c', '--mean-concepts', type=float, default=1.33)
    parser.add_argument('-s', '--smoothing', type=float, default=0.01)
    parser.add_argument('-t', '--generation-type', choices=['random', 'histogram', 'roulette'], default='roulette')
    parser.add_argument('-p', '--prettify', action='store_true')

    parser.add_argument('--no-extra-files', action='store_true')

    parser.add_argument('-f', '--results-folder', default='results')

    args = parser.parse_args()

    with open(args.characteristics_file, 'rb') as file:
        stats = pickle.load(file)

    (materials_list, lom_data) = generate_materials(stats, args.number_materials, args.generation_type, args)

    os.makedirs(args.results_folder, exist_ok=True)
    os.makedirs(os.path.join(args.results_folder, 'LOM'), exist_ok=True)

    write_material_coverage_file(os.path.join(args.results_folder, 'material_coverage.csv'), materials_list)
    write_lom_file(os.path.join(args.results_folder, 'LOM'), lom_data, args.prettify)

    if not args.no_extra_files:
        write_instance_file(args.results_folder, stats,
                            instance_name='instance.txt',
                            parameters_name='parameters.txt',
                            concepts_name='concepts.csv',
                            learners_name='learners.csv',
                            score_name='learners_score.csv',
                            coverage_name='material_coverage.csv',
                            lom_name='LOM')
