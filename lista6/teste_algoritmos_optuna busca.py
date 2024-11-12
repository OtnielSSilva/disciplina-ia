import heapq
import random
from scipy.stats import t
import numpy as np


def heuristica(nodo, objetivo, tipo='manhattan'):
    if tipo == 'manhattan':
        distancia = 0
        for i in range(1, 9):
            xi, yi = divmod(nodo.index(i), 3)
            xg, yg = divmod(objetivo.index(i), 3)
            distancia += abs(xi - xg) + abs(yi - yg)
        return distancia
    elif tipo == 'fora_do_lugar':
        return sum([1 if nodo[i] != objetivo[i] else 0 for i in range(9)])
    else:
        return 0


def gerar_sucessores(estado, estado_pai):
    sucessores = []
    indice_zero = estado.index(0)
    movimentos = []
    if indice_zero % 3 > 0:
        movimentos.append(-1)  # mover para a esquerda
    if indice_zero % 3 < 2:
        movimentos.append(1)   # mover para a direita
    if indice_zero // 3 > 0:
        movimentos.append(-3)  # mover para cima
    if indice_zero // 3 < 2:
        movimentos.append(3)   # mover para baixo
    for movimento in movimentos:
        novo_estado = estado.copy()
        indice_troca = indice_zero + movimento
        novo_estado[indice_zero], novo_estado[indice_troca] = novo_estado[indice_troca], novo_estado[indice_zero]
        if novo_estado != estado_pai:
            sucessores.append(novo_estado)
    return sucessores


def busca(estado_inicial, estado_objetivo, algoritmo='gulosa'):
    fronteira = []
    # (prioridade, estado, custo, caminho, estado_pai)
    heapq.heappush(fronteira, (0, estado_inicial, 0, [estado_inicial], None))
    visitados = set()
    explorados = 0
    while fronteira:
        prioridade, estado_atual, custo, caminho, estado_pai = heapq.heappop(
            fronteira)
        estado_tupla = tuple(estado_atual)
        if estado_tupla in visitados:
            continue
        visitados.add(estado_tupla)
        explorados += 1

        if estado_atual == estado_objetivo:
            return explorados  # Retorna o número de nós explorados

        sucessores = gerar_sucessores(
            estado_atual, estado_pai if estado_pai else [])
        for sucessor in sucessores:
            if tuple(sucessor) in visitados:
                continue
            if algoritmo == 'a*':
                g = custo + 1
                h = heuristica(sucessor, estado_objetivo, tipo='manhattan')
                prioridade_sucessor = g + h
            elif algoritmo == 'gulosa':
                h = heuristica(sucessor, estado_objetivo, tipo='manhattan')
                prioridade_sucessor = h
            heapq.heappush(fronteira, (prioridade_sucessor, sucessor,
                           custo+1, caminho + [sucessor], estado_atual))
    return None  # Falha ao encontrar solução

# Função para realizar várias execuções e calcular estatísticas


def executar_testes(repeticoes, estado_inicial, estado_objetivo, algoritmo):
    nos_explorados = []
    for _ in range(repeticoes):
        estado_embaralhado = estado_inicial[:]
        # Embaralha o estado inicial para cada execução
        random.shuffle(estado_embaralhado)
        explorados = busca(estado_embaralhado,
                           estado_objetivo, algoritmo=algoritmo)
        if explorados is not None:
            nos_explorados.append(explorados)

    # Cálculo da média e intervalo de confiança
    media = np.mean(nos_explorados)
    desvio_padrao = np.std(nos_explorados, ddof=1)
    n = len(nos_explorados)
    t_score = t.ppf(1 - 0.025, df=n - 1)  # Intervalo de confiança de 95%
    margem_erro = t_score * (desvio_padrao / np.sqrt(n))
    intervalo_conf = (media - margem_erro, media + margem_erro)

    print(f"Algoritmo: {algoritmo}")
    print(f"Média de nós explorados: {media}")
    print(f"Desvio padrão: {desvio_padrao}")
    print(f"Intervalo de confiança (95%): {intervalo_conf}")
    print("-------------------------")


# Estado inicial e objetivo
estado_inicial = [3, 1, 2,
                  0, 4, 5,
                  6, 7, 8]

estado_objetivo = [0, 1, 2,
                   3, 4, 5,
                   6, 7, 8]

# Executar testes para busca Gulosa e A*
executar_testes(50, estado_inicial, estado_objetivo, algoritmo='gulosa')
executar_testes(50, estado_inicial, estado_objetivo, algoritmo='a*')
