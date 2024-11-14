import random
import math
import numpy as np
import time
from scipy.stats import mannwhitneyu

# Parâmetros fixos para Simulated Annealing
TEMPERATURA_INICIAL = 2228.7334309974863
TAXA_RESFRIAMENTO = 0.99879992813009228
N_QUEENS = 16
MAX_FITNESS = int(N_QUEENS * (N_QUEENS - 1) / 2)


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
    tabuleiro_atual = tabuleiro.copy()
    conflitos_atual = calcular_conflitos(tabuleiro_atual)
    menor_conflito = conflitos_atual
    iteracoes_sem_melhoria = 0
    max_iteracoes = 100000

    while conflitos_atual > 0 and temperatura > 0.1 and iteracoes_sem_melhoria < 1000:
        tabuleiro_vizinho = gerar_vizinho(tabuleiro_atual)
        conflitos_vizinho = calcular_conflitos(tabuleiro_vizinho)
        delta = conflitos_vizinho - conflitos_atual

        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperatura):
            tabuleiro_atual = tabuleiro_vizinho
            conflitos_atual = conflitos_vizinho

            if conflitos_atual < menor_conflito:
                menor_conflito = conflitos_atual
                iteracoes_sem_melhoria = 0
            else:
                iteracoes_sem_melhoria += 1
        else:
            iteracoes_sem_melhoria += 1

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


# Comparação entre Simulated Annealing e Algoritmo Genético 4
simulated_results = []
genetic_results = []
simulated_times = []
genetic_times = []

for i in range(30):
    initial_board = create_individual(N_QUEENS)

    start_time = time.time()
    simulated_conflicts = simulated_annealing(initial_board)
    simulated_times.append(time.time() - start_time)
    simulated_results.append(simulated_conflicts)

    start_time = time.time()
    genetic_conflicts = genetic_algorithm_4(100, 50, initial_board)
    genetic_times.append(time.time() - start_time)
    genetic_results.append(genetic_conflicts)

# Teste Mann-Whitney para diferenças
stat_conflicts, p_value_conflicts = mannwhitneyu(
    simulated_results, genetic_results, alternative="two-sided")
stat_times, p_value_times = mannwhitneyu(
    simulated_times, genetic_times, alternative="two-sided")

# Resultados formatados para cada iteração e estatísticas finais
output = ["Resultados das 30 Iterações:\n"]
output.append(
    f"{'Iteração':<10}{'Conflitos SA':<15}{'Tempo SA (s)':<15}{'Conflitos GA4':<15}{'Tempo GA4 (s)':<15}\n")
for i in range(30):
    output.append(
        f"{i+1:<10}{simulated_results[i]:<15}{simulated_times[i]:<15.6f}{genetic_results[i]:<15}{genetic_times[i]:<15.6f}\n")

# Estatísticas gerais
output.append("\nEstatísticas Gerais:\n")
output.append(
    f"Média de Conflitos (SA): {np.mean(simulated_results):.2f}, Média de Conflitos (GA4): {np.mean(genetic_results):.2f}\n")
output.append(
    f"Média de Tempo (SA): {np.mean(simulated_times):.6f} s, Média de Tempo (GA4): {np.mean(genetic_times):.6f} s\n")
output.append("\nTeste Mann-Whitney para Conflitos:\n")
output.append(
    f"Estatística = {stat_conflicts}, p-valor = {p_value_conflicts}\n")
output.append("Diferença estatisticamente significativa para conflitos.\n" if p_value_conflicts <
              0.05 else "Nenhuma diferença significativa para conflitos.\n")
output.append("\nTeste Mann-Whitney para Tempos:\n")
output.append(f"Estatística = {stat_times}, p-valor = {p_value_times}\n")
output.append("Diferença estatisticamente significativa para tempos.\n" if p_value_times <
              0.05 else "Nenhuma diferença significativa para tempos.\n")

# Salvar em arquivo
with open("resultados_analise_detalhada.txt", "w") as file:
    file.writelines(output)

print("Análise detalhada salva em 'resultados_analise_detalhada.txt'")
