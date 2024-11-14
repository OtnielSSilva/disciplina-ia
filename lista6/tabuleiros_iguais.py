import random
import math
import numpy as np
import time
from scipy.stats import mannwhitneyu

TEMPERATURA_INICIAL = 3500
TAXA_RESFRIAMENTO = 0.998
N_QUEENS = 16
MAX_FITNESS = int(N_QUEENS * (N_QUEENS - 1) / 2)

TEMPERATURA_MINIMA = 0.1
ITERACOES_POR_TEMPERATURA = 100
ITERACOES_SEM_MELHORIA_MAX = 1000


def calcular_conflitos(tabuleiro):
    n = len(tabuleiro)
    conflitos = 0
    linhas = [0] * n
    diag_principal = [0] * (2 * n - 1)
    diag_secundaria = [0] * (2 * n - 1)

    for i in range(n):
        linhas[tabuleiro[i]] += 1
        diag_principal[i + tabuleiro[i]] += 1
        diag_secundaria[n - 1 - i + tabuleiro[i]] += 1

    for i in range(2 * n - 1):
        if diag_principal[i] > 1:
            conflitos += diag_principal[i] - 1
        if diag_secundaria[i] > 1:
            conflitos += diag_secundaria[i] - 1

    for i in range(n):
        if linhas[i] > 1:
            conflitos += linhas[i] - 1

    return conflitos


def gerar_vizinho(tabuleiro):
    n = len(tabuleiro)
    coluna = random.randint(0, n - 1)
    melhor_linha = tabuleiro[coluna]
    menor_conflito = float('inf')

    for linha in range(n):
        if linha != tabuleiro[coluna]:
            novo_tabuleiro = tabuleiro.copy()
            novo_tabuleiro[coluna] = linha
            conflitos = calcular_conflitos(novo_tabuleiro)
            if conflitos < menor_conflito:
                menor_conflito = conflitos
                melhor_linha = linha

    vizinho = tabuleiro.copy()
    vizinho[coluna] = melhor_linha
    return vizinho


def simulated_annealing(tabuleiro):
    temperatura = TEMPERATURA_INICIAL
    tabuleiro_atual = tabuleiro.copy()  # Inicia com o tabuleiro recebido
    conflitos_atual = calcular_conflitos(tabuleiro_atual)
    menor_conflito = conflitos_atual
    iteracoes_sem_melhoria = 0

    while conflitos_atual > 0 and temperatura > TEMPERATURA_MINIMA and iteracoes_sem_melhoria < ITERACOES_SEM_MELHORIA_MAX:
        for _ in range(ITERACOES_POR_TEMPERATURA):
            # Geração do vizinho e cálculo de conflitos
            tabuleiro_vizinho = gerar_vizinho(tabuleiro_atual)
            conflitos_vizinho = calcular_conflitos(tabuleiro_vizinho)
            delta = conflitos_vizinho - conflitos_atual

            # Critério de aceitação de vizinho (baseado na temperatura)
            if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperatura):
                tabuleiro_atual = tabuleiro_vizinho
                conflitos_atual = conflitos_vizinho

                # Atualiza o menor conflito encontrado
                if conflitos_atual < menor_conflito:
                    menor_conflito = conflitos_atual
                    iteracoes_sem_melhoria = 0
                else:
                    iteracoes_sem_melhoria += 1
            else:
                iteracoes_sem_melhoria += 1

        # Resfriamento da temperatura
        temperatura *= TAXA_RESFRIAMENTO

    return menor_conflito


def genetic_algorithm_4(pop_size, generations, tabuleiro):
    mutation_rate = 0.05
    population = [swap_mutation(tabuleiro.copy()) for _ in range(pop_size)]
    best_fitness = float('-inf')

    for _ in range(generations):
        fitnesses = [fitness(ind) for ind in population]
        total_fitness = sum(fitnesses)
        probabilities = [f / total_fitness for f in fitnesses]

        new_population = []
        for _ in range(pop_size):
            parent1 = population[np.random.choice(
                range(pop_size), p=probabilities)]
            parent2 = population[np.random.choice(
                range(pop_size), p=probabilities)]
            child = order_crossover(parent1, parent2)

            if random.random() < mutation_rate:
                child = swap_mutation(child)

            new_population.append(child)

        population = new_population
        best_fitness = max(fitnesses)

    return MAX_FITNESS - best_fitness  # Retorna o número de conflitos

# Funções auxiliares para Algoritmo Genético


def create_individual(n):
    return random.sample(range(n), n)


def fitness(individual):
    return MAX_FITNESS - calcular_conflitos(individual)


def swap_mutation(individual):
    idx1, idx2 = random.sample(range(len(individual)), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual


def order_crossover(parent1, parent2):
    n = len(parent1)
    start, end = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[start:end] = parent1[start:end]
    pos = end % n
    for gene in parent2[end:] + parent2[:end]:
        if gene not in child:
            child[pos] = gene
            pos = (pos + 1) % n
    return child


# Número de configurações iniciais
NUM_INITIAL_BOARDS = 30

# Gera as configurações iniciais
initial_boards = [create_individual(N_QUEENS)
                  for _ in range(NUM_INITIAL_BOARDS)]

# Armazenamento dos resultados
results = []

for idx, initial_board in enumerate(initial_boards):
    simulated_results = []
    genetic_results = []
    simulated_times = []
    genetic_times = []

    for i in range(30):
        board_for_sa = initial_board.copy()
        board_for_ga4 = initial_board.copy()

        # Simulated Annealing
        start_time = time.time()
        simulated_conflicts = simulated_annealing(board_for_sa)
        simulated_time = time.time() - start_time
        simulated_results.append(simulated_conflicts)
        simulated_times.append(simulated_time)

        # Algoritmo Genético 4
        start_time = time.time()
        genetic_conflicts = genetic_algorithm_4(100, 50, board_for_ga4)
        genetic_time = time.time() - start_time
        genetic_results.append(genetic_conflicts)
        genetic_times.append(genetic_time)

    # Teste Mann-Whitney para diferenças
    stat_conflicts, p_value_conflicts = mannwhitneyu(
        simulated_results, genetic_results, alternative="two-sided")
    stat_times, p_value_times = mannwhitneyu(
        simulated_times, genetic_times, alternative="two-sided")

    # Armazena os resultados
    results.append({
        'initial_board_idx': idx+1,
        'simulated_results': simulated_results,
        'genetic_results': genetic_results,
        'simulated_times': simulated_times,
        'genetic_times': genetic_times,
        'stat_conflicts': stat_conflicts,
        'p_value_conflicts': p_value_conflicts,
        'stat_times': stat_times,
        'p_value_times': p_value_times
    })


output = []

for res in results:
    idx = res['initial_board_idx']
    output.append(f"\nResultados para a Configuração de Tabuleiro {idx}:\n")
    output.append("Resultados das 30 Execuções:\n")
    output.append(
        f"{'Execução':<10}{'Conflitos SA':<15}{'Tempo SA (s)':<15}{'Conflitos GA4':<15}{'Tempo GA4 (s)':<15}\n")
    for i in range(30):
        output.append(
            f"{i+1:<10}{res['simulated_results'][i]:<15}{res['simulated_times'][i]:<15.6f}"
            f"{res['genetic_results'][i]:<15}{res['genetic_times'][i]:<15.6f}\n")

    # Estatísticas gerais para esta configuração
    output.append("\nEstatísticas Gerais:\n")
    output.append(
        f"Média de Conflitos (SA): {np.mean(res['simulated_results']):.2f}, "
        f"Média de Conflitos (GA4): {np.mean(res['genetic_results']):.2f}\n")
    output.append(
        f"Média de Tempo (SA): {np.mean(res['simulated_times']):.6f} s, "
        f"Média de Tempo (GA4): {np.mean(res['genetic_times']):.6f} s\n")
    output.append("\nTeste Mann-Whitney para Conflitos:\n")
    output.append(
        f"Estatística = {res['stat_conflicts']}, p-valor = {res['p_value_conflicts']}\n")
    if res['p_value_conflicts'] < 0.05:
        output.append(
            "Diferença estatisticamente significativa para conflitos.\n")
    else:
        output.append("Nenhuma diferença significativa para conflitos.\n")
    output.append("\nTeste Mann-Whitney para Tempos:\n")
    output.append(
        f"Estatística = {res['stat_times']}, p-valor = {res['p_value_times']}\n")
    if res['p_value_times'] < 0.05:
        output.append(
            "Diferença estatisticamente significativa para tempos.\n")
    else:
        output.append("Nenhuma diferença significativa para tempos.\n")

# Salvar em arquivo
with open("resultados_analise_detalhada_iguais.txt", "w") as file:
    file.writelines(output)

print("Análise detalhada salva em 'resultados_analise_detalhada.txt'")
