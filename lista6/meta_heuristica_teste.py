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


def simulated_annealing(n, temperatura_inicial, taxa_resfriamento):
    temperatura = temperatura_inicial
    tabuleiro_atual = [random.randint(0, n - 1) for _ in range(n)]
    conflitos_atual = conflito(tabuleiro_atual)
    melhor_tabuleiro = tabuleiro_atual.copy()
    menor_conflito = conflitos_atual
    iteracao = 0
    max_iteracoes = 10000

    while conflitos_atual > 0 and temperatura > 0.1 and iteracao < max_iteracoes:
        tabuleiro_vizinho = gerar_vizinho(tabuleiro_atual)
        conflitos_vizinho = conflito(tabuleiro_vizinho)
        delta = conflitos_vizinho - conflitos_atual

        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperatura):
            tabuleiro_atual = tabuleiro_vizinho
            conflitos_atual = conflitos_vizinho
            if conflitos_atual < menor_conflito:
                melhor_tabuleiro = tabuleiro_atual.copy()
                menor_conflito = conflitos_atual
        temperatura *= taxa_resfriamento
        iteracao += 1

    return menor_conflito, iteracao, melhor_tabuleiro


def testar_varias_configuracoes(n):
    melhores_resultados = []
    temperaturas = [1000, 2500, 5000]  # Exemplo de temperaturas iniciais
    resfriamentos = [0.995, 0.997, 0.999]  # Exemplo de taxas de resfriamento

    for temperatura in temperaturas:
        for resfriamento in resfriamentos:
            print(
                f"\nTestando com temperatura inicial = {temperatura} e resfriamento = {resfriamento}")
            menor_conflito, iteracoes, tabuleiro_final = simulated_annealing(
                n, temperatura, resfriamento)
            print(f"Menor número de conflitos: {menor_conflito}")
            print(f"Iterações: {iteracoes}")
            melhores_resultados.append({
                "Temperatura": temperatura,
                "Resfriamento": resfriamento,
                "Menor Conflito": menor_conflito,
                "Iterações": iteracoes,
                "Tabuleiro Final": tabuleiro_final
            })


testar_varias_configuracoes(8)
