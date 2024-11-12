import heapq
import random
from scipy.stats import t, kruskal
import numpy as np
import optuna


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


def busca(estado_inicial, estado_objetivo, algoritmo='gulosa', tipo_heuristica='manhattan'):
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
                h = heuristica(sucessor, estado_objetivo, tipo=tipo_heuristica)
                prioridade_sucessor = g + h
            elif algoritmo == 'gulosa':
                h = heuristica(sucessor, estado_objetivo, tipo=tipo_heuristica)
                prioridade_sucessor = h
            heapq.heappush(fronteira, (prioridade_sucessor, sucessor,
                           custo+1, caminho + [sucessor], estado_atual))
    return None  # Falha ao encontrar solução


def executar_testes(repeticoes, estado_inicial, estado_objetivo, algoritmo, tipo_heuristica):
    nos_explorados = []
    for _ in range(repeticoes):
        estado_embaralhado = estado_inicial[:]
        random.shuffle(estado_embaralhado)
        explorados = busca(estado_embaralhado, estado_objetivo,
                           algoritmo=algoritmo, tipo_heuristica=tipo_heuristica)
        if explorados is not None:
            nos_explorados.append(explorados)
    return nos_explorados

# Otimização com Optuna para selecionar a melhor heurística


def objective(trial):
    tipo_heuristica = trial.suggest_categorical(
        "tipo_heuristica", ["manhattan", "fora_do_lugar"])
    gulosa_resultados = executar_testes(
        30, estado_inicial, estado_objetivo, algoritmo='gulosa', tipo_heuristica=tipo_heuristica)
    a_estrela_resultados = executar_testes(
        30, estado_inicial, estado_objetivo, algoritmo='a*', tipo_heuristica=tipo_heuristica)
    return np.mean(gulosa_resultados) + np.mean(a_estrela_resultados)


estado_inicial = [3, 1, 2, 4, 0, 5, 6, 7, 8]
estado_objetivo = [0, 1, 2, 3, 4, 5, 6, 7, 8]

# Executa a otimização com Optuna
study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=10)
melhor_heuristica = study.best_params["tipo_heuristica"]

# Realiza os testes finais com a melhor heurística encontrada
gulosa_resultados = executar_testes(
    30, estado_inicial, estado_objetivo, algoritmo='gulosa', tipo_heuristica=melhor_heuristica)
a_estrela_resultados = executar_testes(
    30, estado_inicial, estado_objetivo, algoritmo='a*', tipo_heuristica=melhor_heuristica)

# Teste Kruskal-Wallis para comparar Gulosa e A*
stat, p_value = kruskal(gulosa_resultados, a_estrela_resultados)

output = [
    f"Melhor Heurística Encontrada: {melhor_heuristica}\n",
    f"Média de nós explorados (Gulosa): {np.mean(gulosa_resultados)}\n",
    f"Média de nós explorados (A*): {np.mean(a_estrela_resultados)}\n",
    "\nTeste Kruskal-Wallis\n",
    f"Estatística: {stat}\n",
    f"Valor-p: {p_value}\n",
]

if p_value < 0.05:
    output.append(
        "Diferença estatisticamente significativa entre as buscas Gulosa e A*.\n")
else:
    output.append(
        "Nenhuma diferença estatisticamente significativa encontrada entre as buscas Gulosa e A*.\n")

# Salva no arquivo busca.txt
with open("busca.txt", "w") as file:
    file.writelines(output)

print("Resultados salvos no arquivo 'busca.txt'")
