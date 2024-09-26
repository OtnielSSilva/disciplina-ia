from collections import deque
from queue import PriorityQueue

# Definição da classe Nó


class Node:
    def __init__(self, estado, pai=None, acao=None, custo=0, profundidade=0):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
        self.profundidade = profundidade

    def __lt__(self, other):
        return self.custo < other.custo

# Função para expandir um nó


def expandir(no, problema):
    sucessores = []
    for resultado, custo in problema.sucessor(no.estado):
        s = Node(
            estado=resultado,
            pai=no,
            acao=resultado,  # Ação aqui é o estado sucessor
            custo=no.custo + custo,
            profundidade=no.profundidade + 1
        )
        sucessores.append(s)
    return sucessores

# Função para extrair a solução


def solucao(no):
    caminho = []
    while no.pai:
        caminho.append(no.acao)
        no = no.pai
    caminho.append(no.estado)  # Adiciona o estado inicial
    return list(reversed(caminho))

# Classe para definir o problema


class Problema:
    def __init__(self, estado_inicial, estado_objetivo, sucessor, custo):
        self.estado_inicial = estado_inicial
        self.estado_objetivo = estado_objetivo
        self.sucessor = sucessor
        self.custo = custo

# Função sucessora para o grafo


def sucessor_grafo(estado):
    grafo = {
        'A': [('B', 3), ('C', 1), ('D', 2)],
        'B': [('A', 3), ('E', 3)],
        'C': [('A', 1), ('G', 0)],
        'D': [('A', 2), ('E', 4), ('F', 4), ('G', 0)],
        'E': [('B', 3), ('D', 4), ('F', 3)],
        'F': [('D', 4), ('E', 3), ('G', 5)],
        'G': [('C', 0), ('D', 0), ('F', 5)]
    }
    return grafo.get(estado, [])

# Função de custo para o grafo


def custo_grafo(acao, estado_atual, estado_sucessor):
    return acao[1]  # O custo é o peso da aresta


# Criando o problema com o grafo
problema_grafo = Problema(
    estado_inicial='A',
    estado_objetivo=lambda x: x == 'F',  # Objetivo: chegar no nó F
    sucessor=sucessor_grafo,
    custo=custo_grafo
)

# Busca em Largura (fila)


def busca_largura(problema):
    borda = deque([Node(problema.estado_inicial)])
    explorados = set()
    while borda:
        no = borda.popleft()
        if problema.estado_objetivo(no.estado):
            return solucao(no)
        if no.estado not in explorados:
            explorados.add(no.estado)
            borda.extend(expandir(no, problema))
    return None

# Busca em Profundidade (pilha)


def busca_profundidade(problema):
    borda = [Node(problema.estado_inicial)]
    explorados = set()
    while borda:
        no = borda.pop()
        if problema.estado_objetivo(no.estado):
            return solucao(no)
        if no.estado not in explorados:
            explorados.add(no.estado)
            borda.extend(expandir(no, problema))
    return None

# Busca de Custo Uniforme (fila de prioridade)


def busca_custo_uniforme(problema):
    borda = PriorityQueue()
    borda.put((0, Node(problema.estado_inicial)))
    explorados = set()
    while not borda.empty():
        _, no = borda.get()
        if problema.estado_objetivo(no.estado):
            return solucao(no)
        if no.estado not in explorados:
            explorados.add(no.estado)
            for sucessor in expandir(no, problema):
                borda.put((sucessor.custo, sucessor))
    return None


# Testando as buscas
solucao_largura = busca_largura(problema_grafo)
print("Solução com Busca em Largura:", solucao_largura)

solucao_profundidade = busca_profundidade(problema_grafo)
print("Solução com Busca em Profundidade:", solucao_profundidade)

solucao_custo_uniforme = busca_custo_uniforme(problema_grafo)
print("Solução com Busca de Custo Uniforme:", solucao_custo_uniforme)
