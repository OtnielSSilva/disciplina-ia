import random
import math
import numpy as np
import time
from scipy.stats import mannwhitneyu

# Definir sementes aleatórias para reprodutibilidade
random.seed(42)
np.random.seed(42)

# Parâmetros fixos
TEMPERATURA_INICIAL = 1000
TAXA_RESFRIAMENTO_INICIAL = 0.97
N_QUEENS = 16
MAX_FITNESS = int(N_QUEENS * (N_QUEENS - 1) / 2)

# Parâmetros de SA aprimorados
ITERACOES_POR_TEMPERATURA = 5
TEMPERATURA_MINIMA = 0.1
ITERACOES_SEM_MELHORIA_MAX = 1000


def calcular_conflitos(tabuleiro):
    """
    Calcula o número de conflitos diagonais em um tabuleiro de N-Rainhas.
    A representação é uma permutação, garantindo que não haja conflitos de linha e coluna.
    """
    n = len(tabuleiro)
    conflitos = 0
    diag_principal = [0] * (2 * n - 1)
    diag_secundaria = [0] * (2 * n - 1)

    for i in range(n):
        diag_principal[i + tabuleiro[i]] += 1
        diag_secundaria[n - 1 - i + tabuleiro[i]] += 1

    for i in range(2 * n - 1):
        if diag_principal[i] > 1:
            conflitos += diag_principal[i] - 1
        if diag_secundaria[i] > 1:
            conflitos += diag_secundaria[i] - 1

    return conflitos


def gerar_vizinho(tabuleiro):
    """
    Gera um vizinho realizando uma troca de duas posições no tabuleiro (permuta).
    """
    n = len(tabuleiro)
    idx1, idx2 = random.sample(range(n), 2)
    vizinho = tabuleiro.copy()
    vizinho[idx1], vizinho[idx2] = vizinho[idx2], vizinho[idx1]
    return vizinho


def inicializar_tabuleiro():
    """
    Inicializa o tabuleiro utilizando uma heurística que coloca cada rainha na posição
    com o menor número de conflitos possíveis.
    """
    tabuleiro = list(range(N_QUEENS))
    random.shuffle(tabuleiro)
    # Heurística simples: ajustar para minimizar conflitos iniciais
    for i in range(N_QUEENS):
        min_conflitos = calcular_conflitos(tabuleiro)
        melhor_linha = tabuleiro[i]
        for linha in range(N_QUEENS):
            if linha != tabuleiro[i]:
                novo_tabuleiro = tabuleiro.copy()
                novo_tabuleiro[i] = linha
                conflitos = calcular_conflitos(novo_tabuleiro)
                if conflitos < min_conflitos:
                    min_conflitos = conflitos
                    melhor_linha = linha
        tabuleiro[i] = melhor_linha
    return tabuleiro


def simulated_annealing():
    """
    Implementação aprimorada do Algoritmo de Simulated Annealing para o problema das N-Rainhas.
    """
    temperatura = TEMPERATURA_INICIAL
    tabuleiro_atual = inicializar_tabuleiro()
    conflitos_atual = calcular_conflitos(tabuleiro_atual)
    menor_conflito = conflitos_atual
    iteracoes_sem_melhoria = 0

    while conflitos_atual > 0 and temperatura > TEMPERATURA_MINIMA and iteracoes_sem_melhoria < ITERACOES_SEM_MELHORIA_MAX:
        for _ in range(ITERACOES_POR_TEMPERATURA):
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

                if conflitos_atual == 0:
                    break  # Solução ótima encontrada
        else:
            iteracoes_sem_melhoria += ITERACOES_POR_TEMPERATURA

        # Resfriamento adaptativo: ajustar a taxa de resfriamento com base na taxa de aceitação
        # Aqui, simplificamos mantendo a taxa fixa, mas você pode implementar ajustes dinâmicos
        temperatura *= TAXA_RESFRIAMENTO_INICIAL

    return menor_conflito


def genetic_algorithm_4(pop_size, generations, elitism_count=2, tournament_size=3):
    """
    Implementação do Algoritmo Genético para o problema das N-Rainhas.
    Inclui elitismo e seleção por torneio.
    """
    mutation_rate = 0.05
    # População inicial com indivíduos aleatórios (permutações)
    population = [create_individual(N_QUEENS) for _ in range(pop_size)]
    best_fitness = float('-inf')

    for generation in range(generations):
        fitnesses = [fitness(ind) for ind in population]
        total_fitness = sum(fitnesses)

        # Elitismo: selecionar os melhores indivíduos para a próxima geração
        sorted_population = [ind for _, ind in sorted(
            zip(fitnesses, population), key=lambda x: x[0], reverse=True)]
        elites = sorted_population[:elitism_count]

        # Seleção por Torneio
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

        # Debug: Print progresso a cada 10 gerações
        # if (generation + 1) % 10 == 0 or generation == 0:
        #     print(
        #         f"Geração {generation + 1}: Melhor Fitness = {current_best_fitness}")

    # Retorna o número de conflitos do melhor indivíduo
    return MAX_FITNESS - best_fitness


def torneio_selection(population, fitnesses, tournament_size):
    """
    Seleção por torneio: seleciona o melhor indivíduo de um subconjunto aleatório da população.
    """
    participantes = random.sample(
        list(zip(population, fitnesses)), tournament_size)
    vencedor = max(participantes, key=lambda x: x[1])[0]
    return vencedor

# Funções auxiliares para Algoritmo Genético


def create_individual(n):
    """
    Cria um indivíduo aleatório representando uma permutação válida para o problema das N-Rainhas.
    """
    return random.sample(range(n), n)


def fitness(individual):
    """
    Calcula o fitness do indivíduo. Quanto menor o número de conflitos, maior o fitness.
    """
    return MAX_FITNESS - calcular_conflitos(individual)


def swap_mutation(individual):
    """
    Realiza uma mutação por troca, trocando duas posições aleatórias no indivíduo.
    """
    mutant = individual.copy()
    idx1, idx2 = random.sample(range(len(mutant)), 2)
    mutant[idx1], mutant[idx2] = mutant[idx2], mutant[idx1]
    return mutant


def order_crossover(parent1, parent2):
    """
    Crossover ordenado (Order Crossover - OX) para indivíduos baseados em permutação.
    """
    n = len(parent1)
    start, end = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[start:end] = parent1[start:end]
    pos = end % n
    for gene in parent2[end:] + parent2[:end]:
        if gene not in child:
            child[pos] = gene
            pos = (pos + 1) % n
    # Preencher quaisquer posições restantes
    for i in range(n):
        if child[i] is None:
            for gene in parent2:
                if gene not in child:
                    child[i] = gene
                    break
    return child


# Comparação entre Simulated Annealing e Algoritmo Genético 4
simulated_results = []
genetic_results = []
simulated_times = []
genetic_times = []

for i in range(30):
    print(f"Execução {i+1}/30")

    # Simulated Annealing
    start_time = time.time()
    simulated_conflicts = simulated_annealing()
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
with open("resultados_analise_detalhada_diferentes2.txt", "w") as file:
    file.writelines(output)

print("Análise detalhada salva em 'resultados_analise_detalhada_diferentes2.txt'")
