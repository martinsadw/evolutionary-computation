import argparse
import os
import pickle
import sys

from acs.instance import Instance
from stats.extract import extract_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('instance_file')
    parser.add_argument('-n', '--results-name', default='results/instance.pickle')

    args = parser.parse_args()

    instance = Instance.load_from_file(args.instance_file)

    instance_data = extract_data(instance)

    os.makedirs(os.path.dirname(args.results_name), exist_ok=True)
    with open(args.results_name, 'wb') as file:
        pickle.dump(instance_data, file)
