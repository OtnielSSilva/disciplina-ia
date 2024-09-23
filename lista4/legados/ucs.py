import heapq
from cidades import cidades_romenia


def ucs(problema, inicio, objetivo):
    # fronteira é uma fila de prioridade (custo, cidade)
    fronteira = [(0, inicio)]
    visitados = set()

    while fronteira:
        custo_atual, cidade_atual = heapq.heappop(fronteira)
        if cidade_atual == objetivo:
            return f"Objetivo {objetivo} encontrado com custo {custo_atual}"

        visitados.add(cidade_atual)

        for vizinho, custo in problema[cidade_atual].items():
            if vizinho not in visitados:
                heapq.heappush(fronteira, (custo_atual + custo, vizinho))

    return "Falha: Objetivo não encontrado."


# Testando UCS
print(ucs(cidades_romenia(), 'Arad', 'Bucharest'))
