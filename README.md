Dataset generation for Adaptive Curricular Sequence
===================================================

This repository contains the codes required to generate learning object datasets for the adaptive curriculum sequencing problem. Some datasets and some evolutionary computation algorithms have been included to perform comparative tests.

This project was organized with the following structure:

```
├─ acs         # Implementation of the dataset reader
├─ algorithms  # Implementation of evolutionary computation algorithms
│  ├─ de          # Differential Evolution
│  ├─ ga          # Genetic Algorithm
│  ├─ ppa_c       # Prey Predator Algorithm Continuous
│  ├─ ppa_d       # Prey Predator Algorithm Discrete
│  └─ pso         # Particle Swarm Optmization
├─ generator   # Implementation of dataset generation algorithms
├─ graphics    # Generation of comparison graphs
├─ instance    # Comparison datasets
├─ irace       # Irace tests for choosing algorithm parameters
├─ runners     # Example scripts
├─ stats       # Comparison of dataset characteristics
└─ utils       # Extra codes
```

Requirements
------------

- Python 3
    - Numpy
    - Matplotlib

You can install the dependencies with the following commands:

```shell
apt install python3-pip python3-tk
pip3 install -r requirements.txt
```

Running the codes
-----------------

### Extracting the characteristics of a dataset

Before generating the learning object dataset, you must extract the characteristics from another dataset. These characteristics will be used in the process of generating the learning objects. An example of the characteristics used in the dataset generation are as follows:

```python
{
    'instance': <acs.instance.Instance object>,
    'concepts_materials': [[False, False, False, ...], ...],
    'concepts_name': ['ICHCC03', 'ICFSOOC01', 'ICHCC01', ...],
    'concepts_quant': [11, 17, 12, ...],
    'concepts_difficulty': [3.0, 2.7, 2.6, ...],
    'count_histogram': [222, 39, 16, 4, 3],
    'n_coocurrence_matrix': [[[11.,  0.,  0., ...], ...], ...],
    'coocurrence_set': [{1: {27, 11}, 2: {20}, 3: {18}, ...}, ...],
    'coocurrence_dict': [{set(1, 11): [...], set(17, 25): [...], ...}, ...],
    'quant_resource_types': [5, 5, 3, ...],
    'quant_resource_types_histogram': [53, 75, 81, 58, 14,  2,  0,  1],
    'resource_types_frequency': {'narrative text': 237, 'figure': 116, 'slide': 114, ...},
    'interactivity_level_frequency': {'very low': 140, 'low': 104, 'medium': 35, 'high': 5},
    'interactivity_type_frequency': {'expositive': 216, 'mixed': 68},
}
```

- `instance`: Instance data used in the results file;
- `concepts_materials`: List of concepts covered by each material. Type is array(num_concepts, num_materials);
- `concepts_name`: Name of each concept. Type is array(num_concepts);
- `concepts_quant`: Quantity of materials covering each concept. Type is array(num_concepts);
- `concepts_difficulty`: Average difficulty of materials covering each concept. Type is array(num_concepts);
- `count_histogram`: Quantity of materials covering a given amount of concepts. Type is array(max_num_concepts_per_material);
- `n_coocurrence_matrix`: Concept cooccurrence matrix filtering by number of concepts covered by the material. Type is array(max_num_concepts_per_material, num_concepts, num_concepts);
- `coocurrence_set`: List of all cooccurrences of concepts. Includes cooccurrences of all sizes. Type is array(max_coocurrence_size). Type of each element is dict(num_combination_concepts);
- `coocurrence_dict`: List of materials with cooccurrences for each set of concepts listed in `coocurrence_set`. Type is array(max_coocurrence_size). Type of each element is dict(num_combination_concepts);
- `quant_resource_types`: Number of resource type tags per material according to LOM. Type is array(num_materials);
- `quant_resource_types`: Number materials with a given amount of resource type tags. Type is array(max_num_resouce_tags_per_material);
- `resource_types_frequency`: Quantity of materials with a given resource type tag according to LOM;
- `interactivity_level_frequency`: Quantity of materials with a given interactivity level according to LOM;
- `interactivity_type_frequency`: Quantity of materials with a given interactivity type according to LOM.

For example, to extract the characteristics of the `real` dataset, run the following command:

```shell
python3 -m characteristics_extraction.py instances/real/instance.txt -n results/instance.pickle
```

### Generation of the learning object dataset



### Choice of parameters

The choice of parameters for each algorithm is made using the irace package.

### Generation of the algorithm comparison file

To generate the algotithm comparison file, just run `generate_comparison.py`. For example, to generate the data for the `real` dataset with 100000 evaluations of the objective function, 5 repetitions and excluding PSO, run the following command:

```shell
python3 -m generate_comparison instances/real/instance.txt -n results/real.pickle -b 100000 -r 5 --no-pso
```

#### Available parameters

The behavior of data generation can be controlled by the following parameters:

- `-r, --repetitions`: Number of times the algorithms will be executed. Multiple repetitions are used to reduce the effects of randomness of the metaheuristics;
- `-b, --cost-budget`: Number of times the objective function is allowed to run for each algorithm. It is used as a stopping criterion;
- `-s, --max-stagnation`: Maximum number of iterations without improving the value of the objective function. It is used as a stopping criterion;
- `-i, --num-iterations`: Number of iterations allowed for each algorithm. It is used as a stopping criterion;
- `-f, --results-format`: Format of the generated data. Can be `simple` or `full`;
- `-n, --results-name`: Name of the generated file;
- `--no-ppad`: Do not run tests for PPAD;
- `--no-pso`: Do not run tests for PSO;
- `--no-ga`: Do not run tests for GA;
- `--no-de`: Do not run tests for DE.

You must specify at least one of the stop criteria (`-b`,` -s` or `-i`). If multiple stopping criteria are defined, the algorithms will be interrupted when the first stopping criterion occurs.

#### Results

There are two data formats available for generating the data for each algorithm:

- `simple`: Returns a tuple `(selected_materials, cost_value, partial_fitness_array)`. Generates smaller files, but includes only the selected learning objects and the partial data of cost values and objective function throughout iterations;
- `full`: Returns a tuple `(selected_materials, cost_value, best_fitness_array, partial_fitness_array, perf_counter_array, process_time_array)`. Generates larger files but, in addition to the data generated by the `simple` format, includes execution time data and value of final objective function (this can be calculated from `partial_fitness_array`).

Example of the information contained in the generated file:

```python
{
    'info': {
        'algorithms': ['ppa_d', 'ga', 'de'],
        'command': 'generate_comparison.py instances/real/instance.txt -n results/real.pickle -b 10 --no-pso',
        'datetime': '2020-03-27 15:06:24.658132',
        'instance': <acs.instance.Instance object>,
        'cost_budget': 100000,
        'max_stagnation': None,
        'num_iterations': None,
        'repetitions': 5,
        'results_format': 'simple',
        'results_name': 'results/real.pickle'
    },
    'ppa_d': [...],
    'ga': [...],
    'de': [...]
}
```

- `algorithms`: List of algorithms included in the results file;
- `command`: Command used to generate the data;
- `datetime`: Data generation date;
- `instance`: Instance data used in the results file;
- `cost_budget`: Value of parameter `-b`;
- `max_stagnation`: Value of parameter `-s`;
- `num_iterations`: Value of parameter `-i`;
- `repetitions`: Value of parameter `-r`;
- `results_format`: Value of parameter `-f`;
- `results_name`: Value of parameter `-n`;
- `ppa_d`, `pso`, `ga` e `de`: Data generated by each of the algorithms.


### Graph generation

The codes used to generate the graphs are in the `graphics` folder. They all depend on generating the algorithm comparison file beforehand.

Datasets
--------

All datasets are located in the `instances` folder.
