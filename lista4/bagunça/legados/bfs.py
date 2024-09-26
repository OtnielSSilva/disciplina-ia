from collections import deque
from cidades import cidades_romenia


def bfs(problema, inicio, objetivo):
    fronteira = deque([[inicio]])  # Lista que armazena o caminho completo
    visitados = set()

    while fronteira:
        caminho = fronteira.popleft()  # Extrai o primeiro caminho da fila
        cidade_atual = caminho[-1]  # Última cidade no caminho atual

        if cidade_atual == objetivo:
            return f"Caminho encontrado: {caminho}"

        if cidade_atual not in visitados:
            visitados.add(cidade_atual)

            for vizinho in problema[cidade_atual]:
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                fronteira.append(novo_caminho)

    return "Falha: Objetivo não encontrado."


# Testando BFS corrigido
print(bfs(cidades_romenia(), 'Arad', 'Bucharest'))
