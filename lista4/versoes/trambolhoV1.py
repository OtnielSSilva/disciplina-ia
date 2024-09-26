from collections import deque
import heapq


class Node:
    def __init__(self, estado, pai=None, acao=None, custo=0, profundidade=0):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
        self.profundidade = profundidade

    def __lt__(self, other):
        return self.custo < other.custo


def solucao(no):
    caminho = []
    while no:
        caminho.append(no.estado)
        no = no.pai
    return list(reversed(caminho))


def expandir(no, problema):
    sucessores = []
    for acao, custo in problema.sucessor(no.estado):
        filho = Node(
            estado=acao,
            pai=no,
            acao=acao,
            custo=no.custo + custo,
            profundidade=no.profundidade + 1
        )
        sucessores.append(filho)
    return sucessores


class Problema:
    def __init__(self, estado_inicial, estado_objetivo, sucessor, custo):
        self.estado_inicial = estado_inicial
        self.estado_objetivo = estado_objetivo
        self.sucessor = sucessor
        self.custo = custo


def sucessor_grafo(estado, grafo):
    return grafo.get(estado, [])


def custo_grafo(estado, acao):
    return acao[1]


# Implementação dos algoritmos de busca

def busca_largura(problema):
    borda = deque([Node(problema.estado_inicial)])
    explorados = set()
    estados_na_borda = set([problema.estado_inicial])

    while borda:
        no = borda.popleft()
        estados_na_borda.remove(no.estado)

        if problema.estado_objetivo(no.estado):
            return solucao(no)

        explorados.add(no.estado)

        for filho in expandir(no, problema):
            if filho.estado not in explorados and filho.estado not in estados_na_borda:
                borda.append(filho)
                estados_na_borda.add(filho.estado)

    return None


def busca_profundidade(problema):
    borda = [Node(problema.estado_inicial)]
    explorados = set()
    estados_na_borda = set([problema.estado_inicial])

    while borda:
        no = borda.pop()
        estados_na_borda.remove(no.estado)

        if problema.estado_objetivo(no.estado):
            return solucao(no)

        explorados.add(no.estado)

        for filho in reversed(expandir(no, problema)):
            if filho.estado not in explorados and filho.estado not in estados_na_borda:
                borda.append(filho)
                estados_na_borda.add(filho.estado)

    return None


def busca_custo_uniforme(problema):
    borda = []
    heapq.heappush(borda, (0, Node(problema.estado_inicial)))
    explorados = {}
    estados_na_borda = {problema.estado_inicial: 0}

    while borda:
        custo_atual, no = heapq.heappop(borda)

        if problema.estado_objetivo(no.estado):
            return solucao(no)

        if no.estado not in explorados or custo_atual < explorados[no.estado]:
            explorados[no.estado] = custo_atual
            for sucessor in expandir(no, problema):
                estado_sucessor = sucessor.estado
                custo_sucessor = sucessor.custo
                if estado_sucessor not in explorados or custo_sucessor < explorados.get(estado_sucessor, float('inf')):
                    heapq.heappush(borda, (custo_sucessor, sucessor))
                    estados_na_borda[estado_sucessor] = custo_sucessor

    return None


def busca_profundidade_limitada(problema, limite):
    def recursive_dls(no, problema, limite):
        if problema.estado_objetivo(no.estado):
            return solucao(no), False  # False indica que não houve corte

        elif limite == 0:
            return None, True  # True indica corte (CUT-OFF)

        else:
            cutoff_occurred = False
            for filho in expandir(no, problema):
                resultado, cutoff = recursive_dls(filho, problema, limite - 1)
                if cutoff:
                    cutoff_occurred = True
                elif resultado is not None:
                    return resultado, False
            return None, cutoff_occurred

    no_inicial = Node(problema.estado_inicial)
    resultado, cutoff = recursive_dls(no_inicial, problema, limite)

    if resultado:
        return resultado
    elif cutoff:
        return None
    else:
        return None


# Definição do grafo das cidades
cidades = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Fagaras': [('Sibiu', 99), ('Bucareste', 211)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Pitesti', 97), ('Craiova', 146)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucareste', 101)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
    'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Bucareste': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu': [('Bucareste', 90)],
    'Urziceni': [('Bucareste', 85), ('Hirsova', 98), ('Vaslui', 142)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)]
}

problema_cidades = Problema(
    estado_inicial='Arad',
    estado_objetivo=lambda x: x == 'Bucareste',
    sucessor=lambda estado: sucessor_grafo(estado, cidades),
    custo=custo_grafo
)

# Definição do grafo genérico
grafo = {
    'A': [('B', 3), ('C', 1), ('D', 2)],
    'B': [('A', 3), ('E', 3)],
    'C': [('A', 1), ('G', 0)],
    'D': [('A', 2), ('E', 4), ('F', 4), ('G', 0)],
    'E': [('B', 3), ('D', 4), ('F', 3)],
    'F': [('D', 4), ('E', 3), ('G', 5)],
    'G': [('C', 0), ('D', 0), ('F', 5)]
}

problema_grafo1 = Problema(
    estado_inicial='A',
    estado_objetivo=lambda x: x == 'F',
    sucessor=lambda estado: sucessor_grafo(estado, grafo),
    custo=custo_grafo
)


# Testando as buscas no grafo das cidades
print("=== Testando no Grafo das Cidades ===")
print("\nBusca em Largura:")
solucao_largura_cidades = busca_largura(problema_cidades)
print("Solução:", solucao_largura_cidades)

print("\nBusca em Profundidade:")
solucao_profundidade_cidades = busca_profundidade(problema_cidades)
print("Solução:", solucao_profundidade_cidades)

print("\nBusca de Custo Uniforme:")
solucao_custo_uniforme_cidades = busca_custo_uniforme(problema_cidades)
print("Solução:", solucao_custo_uniforme_cidades)

print("\nBusca em Profundidade Limitada:")
limite = 5
solucao_profundidade_limitada_cidades = busca_profundidade_limitada(
    problema_cidades, limite)
print("Solução:", solucao_profundidade_limitada_cidades)


# Testando as buscas no grafo genérico
print("\n\n=== Testando no Grafo Genérico ===")
print("\nBusca em Largura:")
solucao_largura_grafo1 = busca_largura(problema_grafo1)
print("Solução:", solucao_largura_grafo1)

print("\nBusca em Profundidade:")
solucao_profundidade_grafo1 = busca_profundidade(problema_grafo1)
print("Solução:", solucao_profundidade_grafo1)

print("\nBusca de Custo Uniforme:")
solucao_custo_uniforme_grafo1 = busca_custo_uniforme(problema_grafo1)
print("Solução:", solucao_custo_uniforme_grafo1)

print("\nBusca em Profundidade Limitada:")
limite = 3
solucao_profundidade_limitada_grafo1 = busca_profundidade_limitada(
    problema_grafo1, limite)
print("Solução:", solucao_profundidade_limitada_grafo1)
