from collections import deque
import heapq  # Usado para a implementação da fila de prioridade

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

# Função para expandir um nó


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
    while no is not None:
        caminho.append(no.estado)
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


def busca_largura(problema):
    borda = deque([Node(problema.estado_inicial)])
    explorados = set()
    estados_na_borda = set([problema.estado_inicial])
    nos_expandidos = 0

    while borda:
        no = borda.popleft()
        estados_na_borda.remove(no.estado)
        nos_expandidos += 1

        if problema.estado_objetivo(no.estado):
            print(f"Quantidade de nós expandidos: {nos_expandidos}")
            print(f"Número de nós na BORDA: {len(borda)}")
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
    nos_expandidos = 0

    while borda:
        no = borda.pop()
        estados_na_borda.remove(no.estado)
        nos_expandidos += 1

        if problema.estado_objetivo(no.estado):
            print(f"Quantidade de nós expandidos: {nos_expandidos}")
            print(f"Número de nós na BORDA: {len(borda)}")
            return solucao(no)

        explorados.add(no.estado)

        for filho in expandir(no, problema):
            if filho.estado not in explorados and filho.estado not in estados_na_borda:
                borda.append(filho)
                estados_na_borda.add(filho.estado)

    return None


def busca_custo_uniforme(problema):
    borda = []
    heapq.heappush(borda, (0, Node(problema.estado_inicial)))
    explorados = {}
    nos_expandidos = 0

    while borda:
        custo_atual, no = heapq.heappop(borda)
        nos_expandidos += 1

        if problema.estado_objetivo(no.estado):
            print(f"Quantidade de nós expandidos: {nos_expandidos}")
            print(f"Número de nós na BORDA: {len(borda)}")
            return solucao(no)

        if no.estado not in explorados or custo_atual < explorados[no.estado]:
            explorados[no.estado] = custo_atual
            for sucessor in expandir(no, problema):
                heapq.heappush(borda, (sucessor.custo, sucessor))

    return None


# Testando as buscas
print("Busca em Largura:")
solucao_largura = busca_largura(problema_grafo)
print("Solução:", solucao_largura)

print("\nBusca em Profundidade:")
solucao_profundidade = busca_profundidade(problema_grafo)
print("Solução:", solucao_profundidade)

print("\nBusca de Custo Uniforme:")
solucao_custo_uniforme = busca_custo_uniforme(problema_grafo)
print("Solução:", solucao_custo_uniforme)
