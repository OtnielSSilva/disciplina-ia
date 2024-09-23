from cidades import cidades_romenia


def dfs(problema, inicio, objetivo, caminho=None, visitados=None):
    if caminho is None:
        caminho = [inicio]
    if visitados is None:
        visitados = set()

    cidade_atual = caminho[-1]
    if cidade_atual == objetivo:
        return f"Caminho encontrado: {caminho}"

    visitados.add(cidade_atual)

    for vizinho in problema[cidade_atual]:
        if vizinho not in visitados:
            novo_caminho = list(caminho)
            novo_caminho.append(vizinho)
            resultado = dfs(problema, vizinho, objetivo,
                            novo_caminho, visitados)
            if resultado:
                return resultado

    return None


# Testando DFS corrigido
print(dfs(cidades_romenia(), 'Arad', 'Bucharest'))
