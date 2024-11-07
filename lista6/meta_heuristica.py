import random
import math


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


def gerar_vizinho(tabuleiro):
    n = len(tabuleiro)
    vizinho = tabuleiro.copy()
    coluna = random.randint(0, n - 1)
    nova_linha = random.randint(0, n - 1)
    vizinho[coluna] = nova_linha
    return vizinho


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


def simulated_annealing(n):
    temperatura = 2500
    resfriamento = 0.997
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
        if impressoes < 2:
            print(f"Iteração {iteracao}")
            imprimir_tabuleiro(tabuleiro_vizinho)
            impressoes += 1

        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperatura):
            tabuleiro_atual = tabuleiro_vizinho
            conflitos_atual = conflitos_vizinho
            if conflitos_atual < menor_conflito:
                melhor_tabuleiro = tabuleiro_atual.copy()
                menor_conflito = conflitos_atual
        temperatura *= resfriamento
        iteracao += 1

    # Imprime o tabuleiro final
    print("\nTabuleiro final:")
    imprimir_tabuleiro(melhor_tabuleiro)
    if menor_conflito == 0:
        print("Solução encontrada na iteração", iteracao)
    else:
        print("Falha ao encontrar solução. Menor número de conflitos:", menor_conflito)


# Exemplo de uso com 8 rainhas
simulated_annealing(8)
