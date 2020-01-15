import sys
import pickle

import numpy as np
import matplotlib.pyplot as plt

from acs.objective import fitness
from acs.instance import Instance, print_instance

from utils.misc import evaluate_population_fixed, evaluate_population_random
from utils.runner import run_method

from ppa_b.main import prey_predator_algorithm_binary
from ppa_c.main import prey_predator_algorithm_continuous
from pso.main import particle_swarm_optmization
from ga.main import genetic_algorithm
from de.main import differential_evolution

import ppa_b.config
import ppa_c.config
import pso.config
import ga.config
import de.config


if __name__ == "__main__":
    instance_config_filename = None
    if (len(sys.argv) >= 2):
        instance_config_filename = sys.argv[1]

    if instance_config_filename is None:
        instance = Instance.load_test()
    else:
        instance = Instance.load_from_file(instance_config_filename)

    config_ppa_b = ppa_b.config.Config.load_from_file("instances/ppa_b_config.txt")
    config_ppa_c = ppa_c.config.Config.load_from_file("instances/ppa_c_config.txt")
    config_pso = pso.config.Config.load_from_file("instances/pso_config.txt")
    config_ga = ga.config.Config.load_from_file("instances/ga_config.txt")
    config_de = de.config.Config.load_from_file("instances/de_config.txt")

    config_ppa_b.cost_budget = 100000
    config_ppa_c.cost_budget = 100000
    config_pso.cost_budget = 100000
    config_ga.cost_budget = 100000
    config_de.cost_budget = 100000

    num_repetitions = 5

    use_cache = False
    filename = 'results/2020-01-14_andre_500_5_100000.pickle'

    if not use_cache:
        results_ppa_b = run_method(prey_predator_algorithm_binary, fitness, instance, config_ppa_b, num_repetitions)
        results_ppa_c = run_method(prey_predator_algorithm_continuous, fitness, instance, config_ppa_c, num_repetitions)
        results_pso = run_method(particle_swarm_optmization, fitness, instance, config_pso, num_repetitions)
        results_ga = run_method(genetic_algorithm, fitness, instance, config_ga, num_repetitions)
        results_de = run_method(differential_evolution, fitness, instance, config_de, num_repetitions)

        results = {
            'ppa_b': results_ppa_b,
            'ppa_c': results_ppa_c,
            'pso': results_pso,
            'ga': results_ga,
            'de': results_de,
        }
        with open(filename, 'wb') as file:
            pickle.dump(results, file)
    else:
        with open(filename, 'rb') as file:
            results = pickle.load(file)

        results_ppa_b = results['ppa_b']
        results_ppa_c = results['ppa_c']
        results_pso = results['pso']
        results_ga = results['ga']
        results_de = results['de']

    fitness_ppa_b = np.sum(results_ppa_b[2], axis=3)
    fitness_ppa_c = np.sum(results_ppa_c[2], axis=3)
    fitness_pso = np.sum(results_pso[2], axis=3)
    fitness_ga = np.sum(results_ga[2], axis=3)
    fitness_de = np.sum(results_de[2], axis=3)

    mean_ppa_b = np.mean(fitness_ppa_b, axis=(0, 1))
    mean_ppa_c = np.mean(fitness_ppa_c, axis=(0, 1))
    mean_pso = np.mean(fitness_pso, axis=(0, 1))
    mean_ga = np.mean(fitness_ga, axis=(0, 1))
    mean_de = np.mean(fitness_de, axis=(0, 1))

    student_mean_ppa_b = np.mean(fitness_ppa_b, axis=0)
    student_mean_ppa_c = np.mean(fitness_ppa_c, axis=0)
    student_mean_pso = np.mean(fitness_pso, axis=0)
    student_mean_ga = np.mean(fitness_ga, axis=0)
    student_mean_de = np.mean(fitness_de, axis=0)

    deviation_ppa_b = np.std(fitness_ppa_b, axis=(0, 1))
    deviation_ppa_c = np.std(fitness_ppa_c, axis=(0, 1))
    deviation_pso = np.std(fitness_pso, axis=(0, 1))
    deviation_ga = np.std(fitness_ga, axis=(0, 1))
    deviation_de = np.std(fitness_de, axis=(0, 1))

    mean_partial_ppa_b = np.mean(results_ppa_b[2], axis=(0, 1))
    mean_partial_ppa_c = np.mean(results_ppa_c[2], axis=(0, 1))
    mean_partial_pso = np.mean(results_pso[2], axis=(0, 1))
    mean_partial_ga = np.mean(results_ga[2], axis=(0, 1))
    mean_partial_de = np.mean(results_de[2], axis=(0, 1))

    student_mean_partial_ppa_b = np.mean(results_ppa_b[2], axis=0)
    student_mean_partial_ppa_c = np.mean(results_ppa_c[2], axis=0)
    student_mean_partial_pso = np.mean(results_pso[2], axis=0)
    student_mean_partial_ga = np.mean(results_ga[2], axis=0)
    student_mean_partial_de = np.mean(results_de[2], axis=0)

    factor = np.empty((student_mean_ga.shape[0], 1))
    for i in range(student_mean_ga.shape[0]):
        factor[i] = min(np.min(student_mean_ppa_b[i]),
                        np.min(student_mean_ppa_c[i]),
                        np.min(student_mean_pso[i]),
                        np.min(student_mean_ga[i]),
                        np.min(student_mean_de[i])
                        )

    # Colorblind colors: https://gist.github.com/thriveth/8560036
    # plt.xlabel('# execuções da função de avaliação')
    # plt.ylabel('valor da avaliação')
    # plt.plot(results_ppa_b[1], mean_ppa_b, color='#4daf4a', label="APPD")
    # plt.plot(results_ppa_c[1], mean_ppa_c, color='#f781bf', label="APPC")
    # plt.plot(results_pso[1], mean_pso, color='#a65628', label="OEP")
    # plt.plot(results_ga[1], mean_ga, color='#377eb8', label="AG")
    # plt.plot(results_de[1], mean_de, color='#ff7f00', label="ED")
    # plt.legend(loc=1)
    # plt.show()

    ############################################################################
    # Gerar resultados normalizados para cada aluno
    ############################################################################
    # for i in range(student_mean_ga.shape[0]):
    #     fig = plt.figure()
    #     fig.suptitle('Fitness aluno #%d' % (i))
    #     plt.xlabel('# execuções da função de avaliação')
    #     plt.ylabel('valor da avaliação')
    #     plt.ylim((0.8, 5))
    #     plt.plot(results_ppa_b[1], student_mean_ppa_b[i] / factor[i], color='#4daf4a', label="APPD")
    #     plt.plot(results_ppa_c[1], student_mean_ppa_c[i] / factor[i], color='#f781bf', label="APPC")
    #     plt.plot(results_pso[1], student_mean_pso[i] / factor[i], color='#a65628', label="OEP")
    #     plt.plot(results_ga[1], student_mean_ga[i] / factor[i], color='#377eb8', label="AG")
    #     plt.plot(results_de[1], student_mean_de[i] / factor[i], color='#ff7f00', label="ED")
    #     plt.legend(loc=1)
    #     plt.savefig('results/all/real_test_%d.png' % (i))
    #     plt.close()
    #     # plt.show()
    ############################################################################

    ############################################################################
    # Gerar resultados normalizados de todos os alunos
    ############################################################################
    # global_mean_ppa_b = np.mean(student_mean_ppa_b / factor, axis=0)
    # global_mean_ppa_c = np.mean(student_mean_ppa_c / factor, axis=0)
    # global_mean_pso = np.mean(student_mean_pso / factor, axis=0)
    # global_mean_ga = np.mean(student_mean_ga / factor, axis=0)
    # global_mean_de = np.mean(student_mean_de / factor, axis=0)
    #
    # # Média normalizada
    # plt.xlabel('# execuções da função de avaliação')
    # plt.ylabel('valor da avaliação')
    # plt.plot(results_ppa_b[1], global_mean_ppa_b, color='#4daf4a', label="APPD")
    # plt.plot(results_ppa_c[1], global_mean_ppa_c, color='#f781bf', label="APPC")
    # plt.plot(results_pso[1], global_mean_pso, color='#a65628', label="OEP")
    # plt.plot(results_ga[1], global_mean_ga, color='#377eb8', label="AG")
    # plt.plot(results_de[1], global_mean_de, color='#ff7f00', label="ED")
    # plt.legend(loc=1)
    # plt.savefig('results/real_test_all.png')
    # plt.close()
    # # plt.show()
    ############################################################################

    ############################################################################
    # Gerar resultados separando os alunos por caracteristica
    ############################################################################
    # title = 'duração'
    # axis = '10h | 100h'
    # mask_0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    # mask_1 = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    #
    # # title = 'estilo de aprendizado'
    # # axis = '11 | -11'
    # # mask_0 = [0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16, 17]
    # # mask_1 = [6, 7, 8, 9, 10, 11, 18, 19, 20, 21, 22, 23]
    #
    # # title = 'conceitos'
    # # axis = 'Todos | Muitos | Poucos'
    # # mask_0 = [0, 1, 6, 7, 12, 13, 18, 19]
    # # mask_1 = [2, 3, 8, 9, 14, 15, 20, 21]
    # # mask_2 = [4, 5, 10, 11, 16, 17, 21, 23]
    #
    # # title = 'habilidade'
    # # axis = 'Baixa | Alta'
    # # mask_0 = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
    # # mask_1 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
    #
    # mean_ppa_b_0 = np.mean((mean_ppa_b / factor)[mask_0], axis=0)
    # mean_ppa_c_0 = np.mean((mean_ppa_c / factor)[mask_0], axis=0)
    # mean_pso_0 = np.mean((mean_pso / factor)[mask_0], axis=0)
    # mean_ga_0 = np.mean((mean_ga / factor)[mask_0], axis=0)
    # mean_de_0 = np.mean((mean_de / factor)[mask_0], axis=0)
    #
    # mean_ppa_b_1 = np.mean((mean_ppa_b / factor)[mask_1], axis=0)
    # mean_ppa_c_1 = np.mean((mean_ppa_c / factor)[mask_1], axis=0)
    # mean_pso_1 = np.mean((mean_pso / factor)[mask_1], axis=0)
    # mean_ga_1 = np.mean((mean_ga / factor)[mask_1], axis=0)
    # mean_de_1 = np.mean((mean_de / factor)[mask_1], axis=0)
    #
    # diff_ppa_b = mean_ppa_b_1 - mean_ppa_b_0
    # diff_ppa_c = mean_ppa_c_1 - mean_ppa_c_0
    # diff_pso = mean_pso_1 - mean_pso_0
    # diff_ga = mean_ga_1 - mean_ga_0
    # diff_de = mean_de_1 - mean_de_0
    #
    # margin = 0.2
    # cut_fac = 0.05
    # ##############
    # ppa_b_lim = max(np.max(diff_ppa_b[int(diff_ppa_b.shape[0] * cut_fac):]), -np.min(diff_ppa_b[int(diff_ppa_b.shape[0] * cut_fac):]))
    # ppa_c_lim = max(np.max(diff_ppa_c[int(diff_ppa_c.shape[0] * cut_fac):]), -np.min(diff_ppa_c[int(diff_ppa_c.shape[0] * cut_fac):]))
    # pso_lim   = max(np.max(  diff_pso[int(  diff_pso.shape[0] * cut_fac):]), -np.min(  diff_pso[int(  diff_pso.shape[0] * cut_fac):]))
    # ga_lim    = max(np.max(   diff_ga[int(   diff_ga.shape[0] * cut_fac):]), -np.min(   diff_ga[int(   diff_ga.shape[0] * cut_fac):]))
    # de_lim    = max(np.max(   diff_de[int(   diff_de.shape[0] * cut_fac):]), -np.min(   diff_de[int(   diff_de.shape[0] * cut_fac):]))
    #
    # lim = np.mean([ppa_b_lim, ppa_c_lim, pso_lim, ga_lim, de_lim]) * (1 + margin)
    # ylim = (-lim, lim)
    #
    # fig = plt.figure()
    # fig.suptitle('Comparação de %s' % title)
    # plt.xlabel('# execuções da função de avaliação')
    # plt.ylabel(axis)
    # plt.ylim(ylim)
    # plt.plot(results_ppa_b[1], mean_ppa_b_1 - mean_ppa_b_0, color='#4daf4a', label="PPAB")
    # plt.plot(results_ppa_c[1], mean_ppa_c_1 - mean_ppa_c_0, color='#f781bf', label="PPAC")
    # plt.plot(results_pso[1], mean_pso_1 - mean_pso_0, color='#a65628', label="PSO")
    # plt.plot(results_ga[1], mean_ga_1 - mean_ga_0, color='#377eb8', label="GA")
    # plt.plot(results_de[1], mean_de_1 - mean_de_0, color='#ff7f00', label="DE")
    # plt.legend(loc=1)
    # plt.show()
    ############################################################################

    ############################################################################
    # Todos os resultados por algoritmo por aluno
    ############################################################################
    # for i in range(fitness_de.shape[1]):
    #     fig = plt.figure()
    #     fig.suptitle('Fitness aluno #%d' % (i))
    #     plt.xlabel('# execuções da função de avaliação')
    #     plt.ylabel('valor da avaliação')
    #     plt.ylim((0.8, 5))
    #     for j in range(fitness_de.shape[0]):
    #         plt.plot(results_de[1], fitness_de[j, i] / factor[i])
    #
    #     plt.savefig('results/de/real_test_%d_de.png' % (i))
    #     plt.close()
    #     # plt.show()
    ############################################################################

    print(mean_partial_ga[0, 0])
    print(mean_partial_ga[0, 1])
    print(mean_partial_ga[0, 2])
    print(mean_partial_ga[0, 3])
    print(mean_partial_ga[0, 4])

    # plt.xlabel('# execuções da função de avaliação')
    # plt.ylabel('valor da avaliação')
    # plt.plot(results_ga[1], mean_ga, color='#377eb8', label="AG")
    # plt.plot(results_ga[1], mean_ga + deviation_ga, linestyle='--', color='#377eb8', linewidth=0.5)
    # plt.plot(results_ga[1], mean_ga - deviation_ga, linestyle='--', color='#377eb8', linewidth=0.5)
    # plt.fill_between(results_ga[1], mean_ga + deviation_ga, mean_ga - deviation_ga, facecolor='#377eb8', alpha=0.2)
    # plt.plot(results_de[1], mean_de, color='#ff7f00', label="ED")
    # plt.plot(results_de[1], mean_de - deviation_de, linestyle='--', color='#ff7f00', linewidth=0.5)
    # plt.plot(results_de[1], mean_de + deviation_de, linestyle='--', color='#ff7f00', linewidth=0.5)
    # plt.fill_between(results_de[1], mean_de + deviation_de, mean_de - deviation_de, facecolor='#ff7f00', alpha=0.2)
    # plt.legend(loc=1)
    # plt.show()

    # plt.xlabel('# execuções da função de avaliação')
    # plt.ylabel('valor da avaliação')
    # plt.plot(results_de[1], mean_partial_de[:, 0], color='#377eb8', label="Cobertura")
    # plt.plot(results_de[1], mean_partial_de[:, 1], color='#ff7f00', label="Dificuldade")
    # plt.plot(results_de[1], mean_partial_de[:, 2], color='#4daf4a', label="Tempo")
    # plt.plot(results_de[1], mean_partial_de[:, 3], color='#f781bf', label="Balanceamento")
    # plt.plot(results_de[1], mean_partial_de[:, 4], color='#a65628', label="Estilo")
    # plt.legend(loc=1)
    # plt.show()

    # for i in range(fitness_de.shape[1]):
    #     plt.xlabel('# execuções da função de avaliação')
    #     plt.ylabel('valor da avaliação')
    #     plt.ylim((-0.5, 10))
    #     plt.plot(results_de[1], student_mean_partial_de[i, :, 0], color='#377eb8', label="Cobertura")
    #     plt.plot(results_de[1], student_mean_partial_de[i, :, 1], color='#ff7f00', label="Dificuldade")
    #     plt.plot(results_de[1], student_mean_partial_de[i, :, 2], color='#4daf4a', label="Tempo")
    #     plt.plot(results_de[1], student_mean_partial_de[i, :, 3], color='#f781bf', label="Balanceamento")
    #     plt.plot(results_de[1], student_mean_partial_de[i, :, 4], color='#a65628', label="Estilo")
    #     plt.legend(loc=1)
    #     plt.savefig('results/de/real_test_%d_de.png' % (i))
    #     plt.close()
    #     # plt.show()

    # fig = plt.figure()
    # fig.suptitle('Materiais selecionados')
    # # plt.hist(results[0], bins=10, range=(0, num_repetitions))
    # plt.bar(np.arange(results_ga[0].shape[2]), results_ga[0].sum(axis=(0, 1)))
    # plt.show()

    # fig = plt.figure()
    # fig.suptitle('Histograma de materiais')
    # # plt.hist(results[0], bins=10, range=(0, num_repetitions))
    # plt.hist(results_ga[0].sum(axis=(0, 1)))
    # plt.show()
