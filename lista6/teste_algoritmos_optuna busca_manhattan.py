import heapq
import random
from scipy.stats import t, kruskal
import numpy as np


def heuristica(nodo, objetivo):
    distancia = 0
    for i in range(1, 9):
        xi, yi = divmod(nodo.index(i), 3)
        xg, yg = divmod(objetivo.index(i), 3)
        distancia += abs(xi - xg) + abs(yi - yg)
    return distancia


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
            return explorados

        sucessores = gerar_sucessores(
            estado_atual, estado_pai if estado_pai else [])
        for sucessor in sucessores:
            if tuple(sucessor) in visitados:
                continue
            if algoritmo == 'a*':
                g = custo + 1
                h = heuristica(sucessor, estado_objetivo)
                prioridade_sucessor = g + h
            elif algoritmo == 'gulosa':
                h = heuristica(sucessor, estado_objetivo)
                prioridade_sucessor = h
            heapq.heappush(fronteira, (prioridade_sucessor, sucessor,
                           custo+1, caminho + [sucessor], estado_atual))
    return None


def executar_testes(repeticoes, estado_inicial, estado_objetivo, algoritmo):
    nos_explorados = []
    for _ in range(repeticoes):
        estado_embaralhado = estado_inicial[:]
        random.shuffle(estado_embaralhado)
        explorados = busca(estado_embaralhado,
                           estado_objetivo, algoritmo=algoritmo)
        if explorados is not None:
            nos_explorados.append(explorados)
    return nos_explorados


estado_inicial = [3, 1, 2, 4, 0, 5, 6, 7, 8]
estado_objetivo = [0, 1, 2, 3, 4, 5, 6, 7, 8]

# Executar testes
gulosa_resultados = executar_testes(
    30, estado_inicial, estado_objetivo, algoritmo='gulosa')
a_estrela_resultados = executar_testes(
    30, estado_inicial, estado_objetivo, algoritmo='a*')

# Teste Kruskal-Wallis
stat, p_value = kruskal(gulosa_resultados, a_estrela_resultados)

print("Média de nós explorados (Gulosa):", np.mean(gulosa_resultados))
print("Média de nós explorados (A*):", np.mean(a_estrela_resultados))
print("\nTeste Kruskal-Wallis")
print("Estatística:", stat)
print("Valor-p:", p_value)
