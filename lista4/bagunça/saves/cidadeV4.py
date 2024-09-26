from collections import deque
import heapq

# Problema 3
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

    def __repr__(self):
        return f"{self.estado}"


# Função para expandir um nó


def expandir(no, problema):
    sucessores = []
    for acao, resultado, custo in problema.sucessor(no.estado):
        custo_total = no.custo + custo
        s = Node(
            estado=resultado,
            pai=no,
            acao=acao,
            custo=custo_total,
            profundidade=no.profundidade + 1
        )
        sucessores.append(s)
    return sucessores


# Função para extrair a solução


def solucao(no):
    caminho = []
    while no is not None:
        caminho.append(no.estado)
        no = no.pai
    return list(reversed(caminho))


# Classe Problema


class Problema:
    def __init__(self, estado_inicial, estado_objetivo, sucessor, custo):
        self.estado_inicial = estado_inicial
        self.estado_objetivo = estado_objetivo
        self.sucessor = sucessor
        self.custo = custo


# Função sucessora para o mapa da Romênia


def sucessor_romenia(estado):
    mapa_romenia = {
        'Arad': [('Ir para Zerind', 'Zerind', 75), ('Ir para Sibiu', 'Sibiu', 140), ('Ir para Timisoara', 'Timisoara', 118)],
        'Zerind': [('Ir para Arad', 'Arad', 75), ('Ir para Oradea', 'Oradea', 71)],
        'Oradea': [('Ir para Zerind', 'Zerind', 71), ('Ir para Sibiu', 'Sibiu', 151)],
        'Sibiu': [('Ir para Arad', 'Arad', 140), ('Ir para Oradea', 'Oradea', 151), ('Ir para Fagaras', 'Fagaras', 99), ('Ir para Rimnicu Vilcea', 'Rimnicu Vilcea', 80)],
        'Fagaras': [('Ir para Sibiu', 'Sibiu', 99), ('Ir para Bucareste', 'Bucareste', 211)],
        'Rimnicu Vilcea': [('Ir para Sibiu', 'Sibiu', 80), ('Ir para Pitesti', 'Pitesti', 97), ('Ir para Craiova', 'Craiova', 146)],
        'Pitesti': [('Ir para Rimnicu Vilcea', 'Rimnicu Vilcea', 97), ('Ir para Craiova', 'Craiova', 138), ('Ir para Bucareste', 'Bucareste', 101)],
        'Timisoara': [('Ir para Arad', 'Arad', 118), ('Ir para Lugoj', 'Lugoj', 111)],
        'Lugoj': [('Ir para Timisoara', 'Timisoara', 111), ('Ir para Mehadia', 'Mehadia', 70)],
        'Mehadia': [('Ir para Lugoj', 'Lugoj', 70), ('Ir para Drobeta', 'Drobeta', 75)],
        'Drobeta': [('Ir para Mehadia', 'Mehadia', 75), ('Ir para Craiova', 'Craiova', 120)],
        'Craiova': [('Ir para Drobeta', 'Drobeta', 120), ('Ir para Rimnicu Vilcea', 'Rimnicu Vilcea', 146), ('Ir para Pitesti', 'Pitesti', 138)],
        'Bucareste': [('Ir para Fagaras', 'Fagaras', 211), ('Ir para Pitesti', 'Pitesti', 101), ('Ir para Giurgiu', 'Giurgiu', 90), ('Ir para Urziceni', 'Urziceni', 85)],
        'Giurgiu': [('Ir para Bucareste', 'Bucareste', 90)],
        'Urziceni': [('Ir para Bucareste', 'Bucareste', 85), ('Ir para Hirsova', 'Hirsova', 98), ('Ir para Vaslui', 'Vaslui', 142)],
        'Hirsova': [('Ir para Urziceni', 'Urziceni', 98), ('Ir para Eforie', 'Eforie', 86)],
        'Eforie': [('Ir para Hirsova', 'Hirsova', 86)],
        'Vaslui': [('Ir para Urziceni', 'Urziceni', 142), ('Ir para Iasi', 'Iasi', 92)],
        'Iasi': [('Ir para Vaslui', 'Vaslui', 92), ('Ir para Neamt', 'Neamt', 87)],
        'Neamt': [('Ir para Iasi', 'Iasi', 87)]
    }
    return mapa_romenia.get(estado, [])


# Função de custo (opcional)


def custo_romenia(acao, estado_atual, estado_sucessor):
    return 0  # O custo já está sendo considerado na função sucessora


# Definição do problema
problema_romenia = Problema(
    estado_inicial='Arad',
    estado_objetivo=lambda x: x == 'Bucareste',
    sucessor=sucessor_romenia,
    custo=custo_romenia
)


# Implementação das buscas


def busca_largura(problema):
    borda = deque([Node(problema.estado_inicial)])
    explorados = set()
    estados_na_borda = set([problema.estado_inicial])

    # Listas para armazenar os nós para impressão
    todos_nos_na_borda = []
    nos_expandidos_list = []

    while borda:
        no = borda.popleft()
        estados_na_borda.remove(no.estado)
        nos_expandidos_list.append(no.estado)

        if problema.estado_objetivo(no.estado):
            borda_final = list(borda)
            print(f"Quantidade de nós expandidos: {len(nos_expandidos_list)}")
            print(f"Número de nós na BORDA final: {len(borda_final)}")
            print(f"Nos na BORDA final: {borda_final}")
            print(f"Todos os nós adicionados na BORDA: {todos_nos_na_borda}")
            print(f"Todos os nós expandidos: {nos_expandidos_list}")
            return solucao(no)

        explorados.add(no.estado)

        for filho in expandir(no, problema):
            if filho.estado not in explorados and filho.estado not in estados_na_borda:
                borda.append(filho)
                estados_na_borda.add(filho.estado)
                todos_nos_na_borda.append(filho.estado)

    return None


def busca_profundidade(problema):
    borda = [Node(problema.estado_inicial)]
    explorados = set()
    estados_na_borda = set([problema.estado_inicial])

    # Listas para armazenar os nós para impressão
    todos_nos_na_borda = []
    nos_expandidos_list = []

    while borda:
        no = borda.pop()
        estados_na_borda.remove(no.estado)
        nos_expandidos_list.append(no.estado)

        if problema.estado_objetivo(no.estado):
            borda_final = list(borda)
            print(f"Quantidade de nós expandidos: {len(nos_expandidos_list)}")
            print(f"Número de nós na BORDA final: {len(borda_final)}")
            print(f"Nos na BORDA final: {borda_final}")
            print(f"Todos os nós adicionados na BORDA: {todos_nos_na_borda}")
            print(f"Todos os nós expandidos: {nos_expandidos_list}")
            return solucao(no)

        explorados.add(no.estado)

        # Reverso para manter a ordem correta na pilha
        for filho in reversed(expandir(no, problema)):
            if filho.estado not in explorados and filho.estado not in estados_na_borda:
                borda.append(filho)
                estados_na_borda.add(filho.estado)
                todos_nos_na_borda.append(filho.estado)

    return None


def busca_custo_uniforme(problema):
    borda = []
    heapq.heappush(borda, (0, Node(problema.estado_inicial)))
    explorados = {}
    estados_na_borda = set([problema.estado_inicial])

    # Listas para armazenar os nós para impressão
    todos_nos_na_borda = []
    nos_expandidos_list = []

    while borda:
        custo_atual, no = heapq.heappop(borda)
        estados_na_borda.remove(no.estado)
        nos_expandidos_list.append(no.estado)

        if problema.estado_objetivo(no.estado):
            borda_final = [n for c, n in borda]
            print(f"Quantidade de nós expandidos: {len(nos_expandidos_list)}")
            print(f"Número de nós na BORDA final: {len(borda_final)}")
            print(f"Nos na BORDA final: {borda_final}")
            print(f"Todos os nós adicionados na BORDA: {todos_nos_na_borda}")
            print(f"Todos os nós expandidos: {nos_expandidos_list}")
            return solucao(no)

        if no.estado not in explorados or custo_atual < explorados[no.estado]:
            explorados[no.estado] = custo_atual
            for sucessor in expandir(no, problema):
                if sucessor.estado not in explorados or sucessor.custo < explorados.get(sucessor.estado, float('inf')):
                    heapq.heappush(borda, (sucessor.custo, sucessor))
                    estados_na_borda.add(sucessor.estado)
                    todos_nos_na_borda.append(sucessor.estado)

    return None


# Testando as buscas
print("Busca em Largura:")
solucao_largura = busca_largura(problema_romenia)
print("Solução:", solucao_largura)

print("\nBusca em Profundidade:")
solucao_profundidade = busca_profundidade(problema_romenia)
print("Solução:", solucao_profundidade)

print("\nBusca de Custo Uniforme:")
solucao_custo_uniforme = busca_custo_uniforme(problema_romenia)
print("Solução:", solucao_custo_uniforme)
