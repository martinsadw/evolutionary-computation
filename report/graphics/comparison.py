import argparse
import os
import pickle

import numpy as np
import matplotlib.pyplot as plt


# Colorblind colors: https://gist.github.com/thriveth/8560036
colors = {
    'PPAD': '#4daf4a',
    'PSO': '#a65628',
    'GA': '#377eb8',
    'DE': '#ff7f00',
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('results_name')

    parser.add_argument('--results-folder', default='results')
    parser.add_argument('--format', default='png')

    parser.add_argument('--save-mean', action='store_true')
    parser.add_argument('--show-mean', action='store_true')

    parser.add_argument('--save-norm-mean', action='store_true')
    parser.add_argument('--show-norm-mean', action='store_true')

    parser.add_argument('--save-global-mean', action='store_true')
    parser.add_argument('--show-global-mean', action='store_true')

    args = parser.parse_args()

    with open(args.results_name, 'rb') as file:
        results = pickle.load(file)

    algorithms = set(results['info']['algorithms'])
    if not set(['ppa_d', 'pso', 'ga', 'de']).issubset(algorithms):
        raise Exception('Results file must contain data from "ppa_d", "pso", "ga" and "de".')

    results_ppa_d = results['ppa_d']
    results_pso = results['pso']
    results_ga = results['ga']
    results_de = results['de']

    fitness_ppa_d = np.sum(results_ppa_d[2], axis=3)
    fitness_pso = np.sum(results_pso[2], axis=3)
    fitness_ga = np.sum(results_ga[2], axis=3)
    fitness_de = np.sum(results_de[2], axis=3)

    mean_ppa_d = np.mean(fitness_ppa_d, axis=(0, 1))
    mean_pso = np.mean(fitness_pso, axis=(0, 1))
    mean_ga = np.mean(fitness_ga, axis=(0, 1))
    mean_de = np.mean(fitness_de, axis=(0, 1))

    student_mean_ppa_d = np.mean(fitness_ppa_d, axis=0)
    student_mean_pso = np.mean(fitness_pso, axis=0)
    student_mean_ga = np.mean(fitness_ga, axis=0)
    student_mean_de = np.mean(fitness_de, axis=0)

    deviation_ppa_d = np.std(fitness_ppa_d, axis=(0, 1))
    deviation_pso = np.std(fitness_pso, axis=(0, 1))
    deviation_ga = np.std(fitness_ga, axis=(0, 1))
    deviation_de = np.std(fitness_de, axis=(0, 1))

    mean_partial_ppa_d = np.mean(results_ppa_d[2], axis=(0, 1))
    mean_partial_pso = np.mean(results_pso[2], axis=(0, 1))
    mean_partial_ga = np.mean(results_ga[2], axis=(0, 1))
    mean_partial_de = np.mean(results_de[2], axis=(0, 1))

    student_mean_partial_ppa_d = np.mean(results_ppa_d[2], axis=0)
    student_mean_partial_pso = np.mean(results_pso[2], axis=0)
    student_mean_partial_ga = np.mean(results_ga[2], axis=0)
    student_mean_partial_de = np.mean(results_de[2], axis=0)

    factor = np.empty((student_mean_ga.shape[0], 1))
    for i in range(student_mean_ga.shape[0]):
        factor[i] = min(np.min(student_mean_ppa_d[i]),
                        np.min(student_mean_pso[i]),
                        np.min(student_mean_ga[i]),
                        np.min(student_mean_de[i])
                        )

    if args.save_mean or args.save_norm_mean or args.save_global_mean:
        os.makedirs(args.results_folder, exist_ok=True)

    ############################################################################
    # Gerar resultados de média de cada algoritmo
    ############################################################################
    if args.save_mean or args.show_mean:
        plt.xlabel('# execuções da função de avaliação')
        plt.ylabel('valor da avaliação')
        plt.plot(results_ppa_d[1], mean_ppa_d, color=colors['PPAD'], label='PPAD')
        plt.plot(results_pso[1], mean_pso, color=colors['PSO'], label='PSO')
        plt.plot(results_ga[1], mean_ga, color=colors['GA'], label='GA')
        plt.plot(results_de[1], mean_de, color=colors['DE'], label='DE')
        plt.legend(loc=1)

        if args.save_mean:
            plt.savefig(os.path.join(args.results_folder, 'mean.%s' % (args.format)))
        if args.show_mean:
            plt.show()
        plt.close()
    ############################################################################

    ############################################################################
    # Gerar resultados normalizados para cada aluno
    ############################################################################
    if args.save_norm_mean or args.show_norm_mean:
        for i in range(student_mean_ga.shape[0]):
            fig = plt.figure()
            fig.suptitle('Fitness aluno #%d' % (i))
            plt.xlabel('# execuções da função de avaliação')
            plt.ylabel('valor da avaliação')
            plt.ylim((0.8, 5))
            plt.plot(results_ppa_d[1], student_mean_ppa_d[i] / factor[i], color=colors['PPAD'], label='PPAD')
            plt.plot(results_pso[1], student_mean_pso[i] / factor[i], color=colors['PSO'], label='PSO')
            plt.plot(results_ga[1], student_mean_ga[i] / factor[i], color=colors['GA'], label='GA')
            plt.plot(results_de[1], student_mean_de[i] / factor[i], color=colors['DE'], label='DE')
            plt.legend(loc=1)

            if args.save_norm_mean:
                plt.savefig(os.path.join(args.results_folder, 'norm_mean_%d.%s' % (i, args.format)))
            if args.show_norm_mean:
                plt.show()
            plt.close()
    ############################################################################

    ############################################################################
    # Gerar resultados normalizados de todos os alunos
    ############################################################################
    if args.save_global_mean or args.show_global_mean:
        global_mean_ppa_d = np.mean(student_mean_ppa_d / factor, axis=0)
        global_mean_pso = np.mean(student_mean_pso / factor, axis=0)
        global_mean_ga = np.mean(student_mean_ga / factor, axis=0)
        global_mean_de = np.mean(student_mean_de / factor, axis=0)

        # Média normalizada
        plt.xlabel('# execuções da função de avaliação')
        plt.ylabel('valor da avaliação')
        plt.plot(results_ppa_d[1], global_mean_ppa_d, color=colors['PPAD'], label='PPAD')
        plt.plot(results_pso[1], global_mean_pso, color=colors['PSO'], label='PSO')
        plt.plot(results_ga[1], global_mean_ga, color=colors['GA'], label='GA')
        plt.plot(results_de[1], global_mean_de, color=colors['DE'], label='DE')
        plt.legend(loc=1)

        if args.save_global_mean:
            plt.savefig(os.path.join(args.results_folder, 'global_mean.%s' % (args.format)))
        if args.show_global_mean:
            plt.show()
        plt.close()
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
    # mean_ppa_d_0 = np.mean((mean_ppa_d / factor)[mask_0], axis=0)
    # mean_ppa_c_0 = np.mean((mean_ppa_c / factor)[mask_0], axis=0)
    # mean_pso_0 = np.mean((mean_pso / factor)[mask_0], axis=0)
    # mean_ga_0 = np.mean((mean_ga / factor)[mask_0], axis=0)
    # mean_de_0 = np.mean((mean_de / factor)[mask_0], axis=0)
    #
    # mean_ppa_d_1 = np.mean((mean_ppa_d / factor)[mask_1], axis=0)
    # mean_ppa_c_1 = np.mean((mean_ppa_c / factor)[mask_1], axis=0)
    # mean_pso_1 = np.mean((mean_pso / factor)[mask_1], axis=0)
    # mean_ga_1 = np.mean((mean_ga / factor)[mask_1], axis=0)
    # mean_de_1 = np.mean((mean_de / factor)[mask_1], axis=0)
    #
    # diff_ppa_d = mean_ppa_d_1 - mean_ppa_d_0
    # diff_ppa_c = mean_ppa_c_1 - mean_ppa_c_0
    # diff_pso = mean_pso_1 - mean_pso_0
    # diff_ga = mean_ga_1 - mean_ga_0
    # diff_de = mean_de_1 - mean_de_0
    #
    # margin = 0.2
    # cut_fac = 0.05
    # ##############
    # ppa_d_lim = max(np.max(diff_ppa_d[int(diff_ppa_d.shape[0] * cut_fac):]), -np.min(diff_ppa_d[int(diff_ppa_d.shape[0] * cut_fac):]))
    # ppa_c_lim = max(np.max(diff_ppa_c[int(diff_ppa_c.shape[0] * cut_fac):]), -np.min(diff_ppa_c[int(diff_ppa_c.shape[0] * cut_fac):]))
    # pso_lim   = max(np.max(  diff_pso[int(  diff_pso.shape[0] * cut_fac):]), -np.min(  diff_pso[int(  diff_pso.shape[0] * cut_fac):]))
    # ga_lim    = max(np.max(   diff_ga[int(   diff_ga.shape[0] * cut_fac):]), -np.min(   diff_ga[int(   diff_ga.shape[0] * cut_fac):]))
    # de_lim    = max(np.max(   diff_de[int(   diff_de.shape[0] * cut_fac):]), -np.min(   diff_de[int(   diff_de.shape[0] * cut_fac):]))
    #
    # lim = np.mean([ppa_d_lim, ppa_c_lim, pso_lim, ga_lim, de_lim]) * (1 + margin)
    # ylim = (-lim, lim)
    #
    # fig = plt.figure()
    # fig.suptitle('Comparação de %s' % title)
    # plt.xlabel('# execuções da função de avaliação')
    # plt.ylabel(axis)
    # plt.ylim(ylim)
    # plt.plot(results_ppa_d[1], mean_ppa_d_1 - mean_ppa_d_0, color='#4daf4a', label="PPAB")
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

    ############################################################################
    # Desvio padrão de todos os alunos
    ############################################################################
    # plt.xlabel('# execuções da função de avaliação')
    # plt.ylabel('valor da avaliação')
    # plt.plot(results_ga[1], mean_ga, color='#377eb8', label="GA")
    # plt.plot(results_ga[1], mean_ga + deviation_ga, linestyle='--', color='#377eb8', linewidth=0.5)
    # plt.plot(results_ga[1], mean_ga - deviation_ga, linestyle='--', color='#377eb8', linewidth=0.5)
    # plt.fill_between(results_ga[1], mean_ga + deviation_ga, mean_ga - deviation_ga, facecolor='#377eb8', alpha=0.2)
    # plt.plot(results_de[1], mean_de, color='#ff7f00', label="DE")
    # plt.plot(results_de[1], mean_de - deviation_de, linestyle='--', color='#ff7f00', linewidth=0.5)
    # plt.plot(results_de[1], mean_de + deviation_de, linestyle='--', color='#ff7f00', linewidth=0.5)
    # plt.fill_between(results_de[1], mean_de + deviation_de, mean_de - deviation_de, facecolor='#ff7f00', alpha=0.2)
    # plt.legend(loc=1)
    # plt.show()
    ############################################################################

    ############################################################################
    # Funções objetivos de todos os alunos
    ############################################################################
    # plt.xlabel('# execuções da função de avaliação')
    # plt.ylabel('valor da avaliação')
    # plt.plot(results_de[1], mean_partial_de[:, 0], color='#377eb8', label="Cobertura")
    # plt.plot(results_de[1], mean_partial_de[:, 1], color='#ff7f00', label="Dificuldade")
    # plt.plot(results_de[1], mean_partial_de[:, 2], color='#4daf4a', label="Tempo")
    # plt.plot(results_de[1], mean_partial_de[:, 3], color='#f781bf', label="Balanceamento")
    # plt.plot(results_de[1], mean_partial_de[:, 4], color='#a65628', label="Estilo")
    # plt.legend(loc=1)
    # plt.show()
    ############################################################################

    # fig = plt.figure()
    # fig.suptitle('Materiais selecionados')
    # # plt.hist(results[0], bins=10, range=(0, args.repetitions))
    # plt.bar(np.arange(results_ga[0].shape[2]), results_ga[0].sum(axis=(0, 1)))
    # plt.show()

    # fig = plt.figure()
    # fig.suptitle('Histograma de materiais')
    # # plt.hist(results[0], bins=10, range=(0, args.repetitions))
    # plt.hist(results_ga[0].sum(axis=(0, 1)))
    # plt.show()
