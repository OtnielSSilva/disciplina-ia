class Problema:
    def __init__(self, estado_inicial, estado_objetivo, sucessor, custo):
        self.estado_inicial = estado_inicial
        self.estado_objetivo = estado_objetivo
        self.sucessor = sucessor
        self.custo = custo

# Função sucessora genérica que aceita um grafo como parâmetro


def sucessor_grafo(estado, grafo):
    return grafo.get(estado, [])

# Função de custo para o grafo


def custo_grafo(acao, estado_atual, estado_sucessor):
    return acao[1]  # O custo é o peso da aresta
