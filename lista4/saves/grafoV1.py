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
        # Para comparar nós pelo custo (necessário para a fila de prioridade)
        return self.custo < other.custo

# Algoritmo 2: Expansão


def expandir(no, problema):
    sucessores = []
    for resultado, custo in problema.sucessor(no.estado):
        s = Node(
            estado=resultado,
            pai=no,
            acao=resultado,  # Ação aqui é o estado sucessor
            custo=no.custo + custo,  # O custo vem diretamente da função sucessora
            profundidade=no.profundidade + 1
        )
        sucessores.append(s)
    return sucessores

# Função para extrair a solução (caminho até o objetivo)


def solucao(no):
    caminho = []
    while no.pai:
        caminho.append(no.acao)
        no = no.pai
    return list(reversed(caminho))

# Classe para definir o problema


class Problema:
    def __init__(self, estado_inicial, estado_objetivo, sucessor, custo):
        self.estado_inicial = estado_inicial
        self.estado_objetivo = estado_objetivo
        self.sucessor = sucessor
        self.custo = custo

# Função sucessora para o grafo (figura 3)


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
    while borda:
        no = borda.popleft()  # Remove o primeiro elemento da fila
        if problema.estado_objetivo(no.estado):
            return solucao(no)  # Retorna a solução se o objetivo for atingido
        # Expande o nó e adiciona os sucessores à fila
        borda.extend(expandir(no, problema))
    return None  # Falha, não encontrou solução

# Busca em Profundidade (pilha)


def busca_profundidade(problema):
    borda = [Node(problema.estado_inicial)]
    while borda:
        no = borda.pop()  # Remove o último elemento da pilha
        if problema.estado_objetivo(no.estado):
            return solucao(no)
        # Expande o nó e adiciona os sucessores à pilha
        borda.extend(expandir(no, problema))
    return None

# Busca de Custo Uniforme (fila de prioridade)


def busca_custo_uniforme(problema):
    borda = PriorityQueue()
    borda.put((0, Node(problema.estado_inicial)))  # (custo, nó)
    while not borda.empty():
        _, no = borda.get()  # Remove o nó com o menor custo
        if problema.estado_objetivo(no.estado):
            return solucao(no)
        for sucessor in expandir(no, problema):
            # Adiciona os sucessores com seu custo acumulado
            borda.put((sucessor.custo, sucessor))
    return None


# Testando as buscas
solucao_largura = busca_largura(problema_grafo)
print("Solução com Busca em Largura:", solucao_largura)

solucao_profundidade = busca_profundidade(problema_grafo)
print("Solução com Busca em Profundidade:", solucao_profundidade)

solucao_custo_uniforme = busca_custo_uniforme(problema_grafo)
print("Solução com Busca de Custo Uniforme:", solucao_custo_uniforme)