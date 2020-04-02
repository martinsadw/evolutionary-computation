import argparse
import os
import pickle
import sys

from acs.instance import Instance
from stats.extract import extract_data

from generator.main import generate_materials
from generator.concepts_selector import write_material_coverage_file
from generator.lom import write_lom_file

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('characteristics_file')

    parser.add_argument('-n', '--number-materials', type=int, default=1000)
    parser.add_argument('-c', '--mean-concepts', type=float, default=1.33)
    parser.add_argument('-s', '--smoothing', type=float, default=0.01)
    parser.add_argument('-t', '--generation-type', choices=['random', 'histogram', 'roulette'], default='roulette')
    parser.add_argument('-p', '--prettify', action='store_true')

    parser.add_argument('-f', '--results-folder', default='results')

    args = parser.parse_args()

    with open('results/instance_stats.pickle', 'rb') as file:
        stats = pickle.load(file)

    (materials_list, lom_data) = generate_materials(stats, args.number_materials, args.generation_type, args)

    os.makedirs(args.results_folder, exist_ok=True)
    os.makedirs(os.path.join(args.results_folder, 'LOM'), exist_ok=True)

    write_material_coverage_file(os.path.join(args.results_folder, 'material_coverage.csv'), materials_list)
    write_lom_file(os.path.join(args.results_folder, 'LOM'), lom_data, args.prettify)
