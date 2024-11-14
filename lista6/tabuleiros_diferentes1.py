import random
import math
import numpy as np
import time
from scipy.stats import mannwhitneyu

# Função para calcular o número de conflitos entre rainhas


def conflito(tabuleiro):
    conflitos = 0
    n = len(tabuleiro)
    for i in range(n):
        for j in range(i+1, n):
            if tabuleiro[i] == tabuleiro[j]:
                conflitos += 1
            elif abs(tabuleiro[i] - tabuleiro[j]) == j - i:
                conflitos += 1
    return conflitos

# Função para gerar um vizinho, alterando a posição de uma rainha aleatoriamente


def gerar_vizinho(tabuleiro):
    n = len(tabuleiro)
    vizinho = tabuleiro.copy()
    coluna = random.randint(0, n - 1)
    nova_linha = random.randint(0, n - 1)
    vizinho[coluna] = nova_linha
    return vizinho

# Função para imprimir o tabuleiro e o número de conflitos


def imprimir_tabuleiro(tabuleiro):
    n = len(tabuleiro)
    for i in range(n):
        linha = ''
        for j in range(n):
            if tabuleiro[j] == i:
                linha += 'X '
            else:
                linha += '. '
        print(linha)
    print("Conflitos:", conflito(tabuleiro))
    print("--------")

# Implementação do algoritmo de Simulated Annealing para o problema das N-Rainhas


def simulated_annealing(n):
    temperatura = 4500
    resfriamento = 0.998
    tabuleiro_atual = [random.randint(0, n - 1) for _ in range(n)]
    conflitos_atual = conflito(tabuleiro_atual)
    melhor_tabuleiro = tabuleiro_atual.copy()
    menor_conflito = conflitos_atual
    iteracao = 0
    max_iteracoes = 10000
    impressoes = 0  # Contador para limitar o número de prints

    while conflitos_atual > 0 and temperatura > 0.1 and iteracao < max_iteracoes:
        tabuleiro_vizinho = gerar_vizinho(tabuleiro_atual)
        conflitos_vizinho = conflito(tabuleiro_vizinho)
        delta = conflitos_vizinho - conflitos_atual

        # Imprime o processo até 2 vezes
        # if impressoes < 2:
        #     print(f"Iteração {iteracao}")
        #     imprimir_tabuleiro(tabuleiro_vizinho)
        #     impressoes += 1

        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperatura):
            tabuleiro_atual = tabuleiro_vizinho
            conflitos_atual = conflitos_vizinho
            if conflitos_atual < menor_conflito:
                melhor_tabuleiro = tabuleiro_atual.copy()
                menor_conflito = conflitos_atual
        temperatura *= resfriamento
        iteracao += 1

    return menor_conflito


# Funções e parâmetros auxiliares para o Algoritmo Genético 4
N_QUEENS = 16
MAX_FITNESS = int(N_QUEENS * (N_QUEENS - 1) / 2)


def create_individual(n):
    return random.sample(range(n), n)


def fitness(individual):
    return MAX_FITNESS - conflito(individual)


def swap_mutation(individual):
    mutant = individual.copy()
    idx1, idx2 = random.sample(range(len(mutant)), 2)
    mutant[idx1], mutant[idx2] = mutant[idx2], mutant[idx1]
    return mutant


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
    for i in range(n):
        if child[i] is None:
            for gene in parent2:
                if gene not in child:
                    child[i] = gene
                    break
    return child


def genetic_algorithm_4(pop_size, generations, elitism_count=2, tournament_size=3):
    mutation_rate = 0.05
    population = [create_individual(N_QUEENS) for _ in range(pop_size)]
    best_fitness = float('-inf')

    for generation in range(generations):
        fitnesses = [fitness(ind) for ind in population]
        total_fitness = sum(fitnesses)

        sorted_population = [ind for _, ind in sorted(
            zip(fitnesses, population), key=lambda x: x[0], reverse=True)]
        elites = sorted_population[:elitism_count]

        new_population = elites.copy()
        while len(new_population) < pop_size:
            parent1 = torneio_selection(population, fitnesses, tournament_size)
            parent2 = torneio_selection(population, fitnesses, tournament_size)
            child = order_crossover(parent1, parent2)

            if random.random() < mutation_rate:
                child = swap_mutation(child)

            new_population.append(child)

        population = new_population

        current_best_fitness = max(fitnesses)
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness

    return MAX_FITNESS - best_fitness


def torneio_selection(population, fitnesses, tournament_size):
    participantes = random.sample(
        list(zip(population, fitnesses)), tournament_size)
    vencedor = max(participantes, key=lambda x: x[1])[0]
    return vencedor


# Comparação entre Simulated Annealing e Algoritmo Genético 4
simulated_results = []
genetic_results = []
simulated_times = []
genetic_times = []

for i in range(50):
    print(f"Execução {i+1}/50")

    # Simulated Annealing
    start_time = time.time()
    simulated_conflicts = simulated_annealing(N_QUEENS)
    simulated_time = time.time() - start_time
    simulated_results.append(simulated_conflicts)
    simulated_times.append(simulated_time)

    # Algoritmo Genético 4
    start_time = time.time()
    genetic_conflicts = genetic_algorithm_4(pop_size=100, generations=50)
    genetic_time = time.time() - start_time
    genetic_results.append(genetic_conflicts)
    genetic_times.append(genetic_time)

    print(
        f"  SA: Conflitos = {simulated_conflicts}, Tempo = {simulated_time:.6f} s")
    print(
        f"  GA4: Conflitos = {genetic_conflicts}, Tempo = {genetic_time:.6f} s\n")

# Teste Mann-Whitney para diferenças
stat_conflicts, p_value_conflicts = mannwhitneyu(
    simulated_results, genetic_results, alternative="two-sided")
stat_times, p_value_times = mannwhitneyu(
    simulated_times, genetic_times, alternative="two-sided")

# Resultados formatados para cada iteração e estatísticas finais
output = ["Resultados das Iterações:\n"]
output.append(
    f"{'Iteração':<10}{'Conflitos SA':<15}{'Tempo SA (s)':<15}{'Conflitos GA4':<15}{'Tempo GA4 (s)':<15}\n")
for i in range(50):
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
with open("resultados_analise_detalhada_diferentes1.txt", "w") as file:
    file.writelines(output)

print("Análise detalhada salva em 'resultados_analise_detalhada_diferentes1.txt'")
