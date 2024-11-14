import random
import math


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


def simulated_annealing(n):
    # Parâmetros do algoritmo
    temperatura_inicial = 1000.0
    temperatura = temperatura_inicial
    resfriamento = 0.97
    max_iteracoes = 100000
    limite_iteracoes_sem_melhoria = 1000
    ITERACOES_POR_TEMPERATURA = 100

    # Inicialização do tabuleiro com uma permutação aleatória
    tabuleiro_atual = list(range(n))
    random.shuffle(tabuleiro_atual)
    conflitos_atual = calcular_conflitos(tabuleiro_atual)
    melhor_tabuleiro = tabuleiro_atual.copy()
    menor_conflito = conflitos_atual
    iteracao = 0
    iteracoes_sem_melhoria = 0

    while conflitos_atual > 0 and temperatura > 0.1 and iteracao < max_iteracoes:
        # Realiza múltiplas iterações na mesma temperatura (forja)
        for _ in range(ITERACOES_POR_TEMPERATURA):
            tabuleiro_vizinho = gerar_vizinho(tabuleiro_atual)
            conflitos_vizinho = calcular_conflitos(tabuleiro_vizinho)
            delta = conflitos_vizinho - conflitos_atual

            # Critério de aceitação
            if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperatura):
                tabuleiro_atual = tabuleiro_vizinho
                conflitos_atual = conflitos_vizinho

                # Verifica se encontrou um tabuleiro com menos conflitos
                if conflitos_atual < menor_conflito:
                    melhor_tabuleiro = tabuleiro_atual.copy()
                    menor_conflito = conflitos_atual
                    iteracoes_sem_melhoria = 0
                else:
                    iteracoes_sem_melhoria += 1
            else:
                iteracoes_sem_melhoria += 1

            iteracao += 1

        # Resfriamento após cada forja
        temperatura *= resfriamento

        # Reinicialização se atingir o limite de iterações sem melhoria
        if iteracoes_sem_melhoria >= limite_iteracoes_sem_melhoria:
            tabuleiro_atual = list(range(n))
            random.shuffle(tabuleiro_atual)
            conflitos_atual = calcular_conflitos(tabuleiro_atual)
            iteracoes_sem_melhoria = 0
            temperatura = temperatura_inicial  # Opcional: reinicia a temperatura

    # Imprime o resultado final
    print("\nTabuleiro final:")
    imprimir_tabuleiro(melhor_tabuleiro)
    if menor_conflito == 0:
        print("Solução encontrada na iteração", iteracao)
    else:
        print("Falha ao encontrar solução. Menor número de conflitos:", menor_conflito)


# Executa o algoritmo para o problema das 16 rainhas
simulated_annealing(16)