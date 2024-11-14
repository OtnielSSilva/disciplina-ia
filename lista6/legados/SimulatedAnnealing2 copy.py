import random
import math


def calcular_conflitos(tabuleiro):
    conflitos = 0
    n = len(tabuleiro)
    for i in range(n):
        for j in range(i + 1, n):
            if tabuleiro[i] == tabuleiro[j] or abs(tabuleiro[i] - tabuleiro[j]) == abs(i - j):
                conflitos += 1
    return conflitos


def gerar_vizinho(tabuleiro):
    n = len(tabuleiro)
    vizinho = tabuleiro.copy()
    num_movimentos = random.randint(1, 2)  # Mover 1 ou 2 rainhas
    for _ in range(num_movimentos):
        coluna = random.randint(0, n - 1)
        linha = random.randint(0, n - 1)
        vizinho[coluna] = linha
    return vizinho


def simulated_annealing(n):
    temperatura_inicial = 1000.0
    temperatura = temperatura_inicial
    limite_iteracoes_sem_melhoria = 5000
    tabuleiro_atual = [random.randint(0, n - 1) for _ in range(n)]
    conflitos_atual = calcular_conflitos(tabuleiro_atual)
    melhor_tabuleiro = tabuleiro_atual.copy()
    menor_conflito = conflitos_atual
    iteracoes_sem_melhoria = 0
    iteracao = 0

    while conflitos_atual > 0 and temperatura > 0.1:
        tabuleiro_vizinho = gerar_vizinho(tabuleiro_atual)
        conflitos_vizinho = calcular_conflitos(tabuleiro_vizinho)
        delta = conflitos_vizinho - conflitos_atual

        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperatura):
            tabuleiro_atual = tabuleiro_vizinho
            conflitos_atual = conflitos_vizinho

            if conflitos_atual < menor_conflito:
                melhor_tabuleiro = tabuleiro_atual.copy()
                menor_conflito = conflitos_atual
                iteracoes_sem_melhoria = 0
            else:
                iteracoes_sem_melhoria += 1
        else:
            iteracoes_sem_melhoria += 1

        if iteracoes_sem_melhoria >= limite_iteracoes_sem_melhoria:
            temperatura = temperatura_inicial  # Reaquece a temperatura
            iteracoes_sem_melhoria = 0

        temperatura = temperatura_inicial / (1 + iteracao)
        iteracao += 1

    print("\nTabuleiro final:")
    imprimir_tabuleiro(melhor_tabuleiro)
    if menor_conflito == 0:
        print("Solução encontrada na iteração", iteracao)
    else:
        print("Falha ao encontrar solução. Menor número de conflitos:", menor_conflito)


def imprimir_tabuleiro(tabuleiro):
    n = len(tabuleiro)
    for i in range(n):
        linha = ''
        for j in range(n):
            if tabuleiro[j] == i:
                linha += 'Q '
            else:
                linha += '. '
        print(linha)
    print("Conflitos:", calcular_conflitos(tabuleiro))
    print("--------")


# Executa o algoritmo para o problema das N rainhas
simulated_annealing(16)
