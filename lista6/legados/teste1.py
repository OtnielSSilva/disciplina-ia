import random
import math
import numpy as np
import time
from scipy.stats import kruskal, t

# Parâmetros gerais
N_QUEENS = 16
MAX_FITNESS = int(N_QUEENS * (N_QUEENS - 1) / 2)

# Função de avaliação de conflitos


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

# Função para gerar vizinho


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

# Função de fitness para Algoritmo Genético


def fitness(individual):
    return MAX_FITNESS - calcular_conflitos(individual)

# Algoritmo Simulated Annealing


def simulated_annealing(tabuleiro, temperatura_inicial, resfriamento):
    temperatura = temperatura_inicial
    limite_iteracoes_sem_melhoria = 1000
    max_iteracoes = 100000

    tabuleiro_atual = tabuleiro.copy()
    conflitos_atual = calcular_conflitos(tabuleiro_atual)
    menor_conflito = conflitos_atual
    iteracoes_sem_melhoria = 0
    iteracao = 0

    while conflitos_atual > 0 and temperatura > 0.1 and iteracao < max_iteracoes:
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

        if iteracoes_sem_melhoria >= limite_iteracoes_sem_melhoria:
            tabuleiro_atual = list(range(N_QUEENS))
            random.shuffle(tabuleiro_atual)
            conflitos_atual = calcular_conflitos(tabuleiro_atual)
            iteracoes_sem_melhoria = 0
            temperatura = temperatura_inicial

        temperatura *= resfriamento
        iteracao += 1

    return menor_conflito

# Funções auxiliares para Algoritmo Genético


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


def genetic_algorithm_4(pop_size, generations, tabuleiro):
    mutation_rate = 0.05
    population = [swap_mutation(tabuleiro.copy()) for _ in range(pop_size)]
    best_fitness = float('-inf')

    for gen in range(generations):
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

    return MAX_FITNESS - best_fitness


# Parâmetros e testes
temperaturas_iniciais = [random.uniform(500, 5000) for _ in range(10)]
taxas_resfriamento = [random.uniform(0.95, 0.999) for _ in range(10)]
resultados = []

for temp_inicial, resfriamento in zip(temperaturas_iniciais, taxas_resfriamento):
    simulated_results = []
    genetic_results = []
    simulated_times = []
    genetic_times = []

    for _ in range(30):
        initial_board = random.sample(range(N_QUEENS), N_QUEENS)

        start_time = time.time()
        simulated_conflicts = simulated_annealing(
            initial_board, temp_inicial, resfriamento)
        simulated_times.append(time.time() - start_time)
        simulated_results.append(simulated_conflicts)

        start_time = time.time()
        genetic_conflicts = genetic_algorithm_4(100, 50, initial_board)
        genetic_times.append(time.time() - start_time)
        genetic_results.append(genetic_conflicts)

    media_conflitos_original = np.mean(simulated_results)
    desvio_conflitos_original = np.std(simulated_results, ddof=1)
    intervalo_conflitos_original = (media_conflitos_original - t.ppf(0.975, 29) * (desvio_conflitos_original / np.sqrt(30)),
                                    media_conflitos_original + t.ppf(0.975, 29) * (desvio_conflitos_original / np.sqrt(30)))

    media_tempo_original = np.mean(simulated_times)
    desvio_tempo_original = np.std(simulated_times, ddof=1)
    intervalo_tempo_original = (media_tempo_original - t.ppf(0.975, 29) * (desvio_tempo_original / np.sqrt(30)),
                                media_tempo_original + t.ppf(0.975, 29) * (desvio_tempo_original / np.sqrt(30)))

    media_conflitos_novo = np.mean(genetic_results)
    desvio_conflitos_novo = np.std(genetic_results, ddof=1)
    intervalo_conflitos_novo = (media_conflitos_novo - t.ppf(0.975, 29) * (desvio_conflitos_novo / np.sqrt(30)),
                                media_conflitos_novo + t.ppf(0.975, 29) * (desvio_conflitos_novo / np.sqrt(30)))

    media_tempo_novo = np.mean(genetic_times)
    desvio_tempo_novo = np.std(genetic_times, ddof=1)
    intervalo_tempo_novo = (media_tempo_novo - t.ppf(0.975, 29) * (desvio_tempo_novo / np.sqrt(30)),
                            media_tempo_novo + t.ppf(0.975, 29) * (desvio_tempo_novo / np.sqrt(30)))

    resultados.append({
        "Temperatura Inicial": temp_inicial,
        "Taxa Resfriamento": resfriamento,
        "Media Conflitos Original": media_conflitos_original,
        "Intervalo Conflitos Original": intervalo_conflitos_original,
        "Media Tempo Original": media_tempo_original,
        "Intervalo Tempo Original": intervalo_tempo_original,
        "Media Conflitos Novo": media_conflitos_novo,
        "Intervalo Conflitos Novo": intervalo_conflitos_novo,
        "Media Tempo Novo": media_tempo_novo,
        "Intervalo Tempo Novo": intervalo_tempo_novo
    })

# Salvando resultados em arquivo
with open("resultados_comparacao.txt", "w") as f:
    for res in resultados:
        f.write(
            f"Temperatura Inicial: {res['Temperatura Inicial']}, Taxa Resfriamento: {res['Taxa Resfriamento']}\n")
        f.write(
            f"Media Conflitos Original: {res['Media Conflitos Original']}, Intervalo Conflitos Original: {res['Intervalo Conflitos Original']}\n")
        f.write(
            f"Media Tempo Original: {res['Media Tempo Original']}, Intervalo Tempo Original: {res['Intervalo Tempo Original']}\n")
        f.write(
            f"Media Conflitos Novo: {res['Media Conflitos Novo']}, Intervalo Conflitos Novo: {res['Intervalo Conflitos Novo']}\n")
        f.write(
            f"Media Tempo Novo: {res['Media Tempo Novo']}, Intervalo Tempo Novo: {res['Intervalo Tempo Novo']}\n")
        f.write("--------------------------------------------------\n")

print("Resultados salvos em 'resultados_comparacao.txt'")
