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


def busca_largura(problema):
    borda = deque([Node(problema.estado_inicial)])

    passos = 0
    print("=== Iniciando Busca em Largura ===\n")

    while borda:
        no = borda.popleft()

        passos += 1
        print(f"Passo {passos}:")

        print(f"Explorando nó: {no.estado} (Custo acumulado: {no.custo})")

        if problema.estado_objetivo(no.estado):
            print("\n=== Objetivo Encontrado ===")
            print(f"Custo total da solução: {no.custo}")
            print(f"Quantidade de nós expandidos: {passos}")
            print(f"Número de nós na BORDA final: {len(borda)}")
            print(f"Borda final: {[n.estado for n in borda]}")
            return solucao(no)

        for filho in expandir(no, problema):
            borda.append(filho)
            print(f"Adicionado à borda: {filho.estado}")

        print(f"Borda atual: {[n.estado for n in borda]}")
        print("")  

    print("Falha: solução não encontrada\n")
    return None


def busca_profundidade(problema):
    borda = [Node(problema.estado_inicial)]

    passos = 0
    print("=== Iniciando Busca em Profundidade ===\n")

    while borda:
        no = borda.pop() 

        passos += 1
        print(f"Passo {passos}:")

        print(f"Explorando nó: {no.estado} (Custo acumulado: {no.custo})")

        if problema.estado_objetivo(no.estado):
            print("\n=== Objetivo Encontrado ===")
            print(f"Custo total da solução: {no.custo}")
            print(f"Quantidade de nós expandidos: {passos}")
            print(f"Número de nós na BORDA final: {len(borda)}")
            print(f"Borda final: {[n.estado for n in borda]}")
            return solucao(no)

        filhos = expandir(no, problema)

        for filho in filhos:
            borda.append(filho)
            print(f"Adicionado à borda: {filho.estado} (Custo: {filho.custo})")

        print(f"Borda atual: {[n.estado for n in borda]}")
        print("") 

    print("Falha: solução não encontrada\n")
    return None


def busca_custo_uniforme(problema):
    borda = []
    heapq.heappush(borda, (0, Node(problema.estado_inicial)))

    passos = 0
    print("=== Iniciando Busca de Custo Uniforme ===\n")

    while borda:
        custo_atual, no = heapq.heappop(borda)

        if problema.estado_objetivo(no.estado):
            print("\n=== Objetivo Encontrado ===")
            print(f"Custo total da solução: {custo_atual}")
            print(f"Quantidade de nós expandidos: {passos}")
            print(f"Número de nós na BORDA final: {len(borda)}")
            print(f"Borda final: {[n.estado for c, n in borda]}")
            return solucao(no)
        
        passos += 1
        print(f"Passo {passos}:")

        print(f"Explorando nó: {no.estado} (Custo acumulado: {custo_atual})")

        for sucessor in expandir(no, problema):
            custo_sucessor = sucessor.custo

            heapq.heappush(borda, (custo_sucessor, sucessor))
            print(f"Adicionado à borda: {sucessor.estado} (Custo: {sucessor.custo})")

        print(f"Borda atual: {[(c, n.estado) for c, n in borda]}")
        print("")  
        
    print("Falha: solução não encontrada\n")
    return None


def busca_profundidade_limitada(problema, limite):
    def bpl(no, limite, passos):
        print(f"Passo {passos}:")
        print(f"Explorando nó: {no.estado} (Custo acumulado: {no.custo}, Profundidade: {no.profundidade})")

        # Verificar se o estado atual é o objetivo
        if problema.estado_objetivo(no.estado):
            print("\n=== Objetivo Encontrado ===")
            print(f"Custo total da solução: {no.custo}")
            print(f"Quantidade de nós expandidos: {passos}")
            print(f"Caminho da solução: {solucao(no)}")
            return solucao(no), passos

        # Se o limite de profundidade for atingido, parar a expansão
        if limite == 0:
            print(f"Limite de profundidade atingido para nó: {no.estado}")
            return None, passos

        # Expandir todos os filhos, mesmo que o estado já tenha sido visitado antes
        for filho in expandir(no, problema):
            resultado, passos = bpl(filho, limite - 1, passos + 1)
            if resultado is not None:
                return resultado, passos

        return None, passos

    no_inicial = Node(problema.estado_inicial, profundidade=0)
    solucao_encontrada, total_passos = bpl(no_inicial, limite, 1)

    if solucao_encontrada:
        print(f"Solução encontrada com {total_passos} passos.")
    else:
        print("Falha: solução não encontrada dentro do limite\n")

    return solucao_encontrada


cidades = {
    'Arad': [('Sibiu', 140), ('Timisoara', 118), ('Zerind', 75)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
    'Oradea': [('Sibiu', 151), ('Zerind', 71)],
    'Sibiu': [('Arad', 140), ('Fagaras', 99), ('Oradea', 151), ('Rimnicu Vilcea', 80)],
    'Fagaras': [('Bucareste', 211), ('Sibiu', 99)],
    'Rimnicu Vilcea': [('Craiova', 146), ('Pitesti', 97), ('Sibiu', 80)],
    'Pitesti': [('Bucareste', 101), ('Craiova', 138), ('Rimnicu Vilcea', 97)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Mehadia', 70), ('Timisoara', 111)],
    'Mehadia': [('Drobeta', 75), ('Lugoj', 70)],
    'Drobeta': [('Craiova', 120), ('Mehadia', 75)],
    'Craiova': [('Drobeta', 120), ('Pitesti', 138), ('Rimnicu Vilcea', 146)],
    'Bucareste': [('Fagaras', 211), ('Giurgiu', 90), ('Pitesti', 101), ('Urziceni', 85)],
    'Giurgiu': [('Bucareste', 90)],
    'Urziceni': [('Bucareste', 85), ('Hirsova', 98), ('Vaslui', 142)],
    'Hirsova': [('Eforie', 86), ('Urziceni', 98)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Iasi', 92), ('Urziceni', 142)],
    'Iasi': [('Neamt', 87), ('Vaslui', 92)],
    'Neamt': [('Iasi', 87)]
}

problema_cidades = Problema(
    estado_inicial='Arad',
    estado_objetivo=lambda x: x == 'Bucareste',
    sucessor=lambda estado: sucessor_grafo(estado, cidades),
    custo=custo_grafo
)

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

print("=== Testando no Grafo das Cidades ===")
print("\nBusca em Largura:")
solucao_largura_cidades = busca_largura(problema_cidades)
print("Solução:", solucao_largura_cidades)

# print("\nBusca em Profundidade:")
# solucao_profundidade_cidades = busca_profundidade(problema_cidades)
# print("Solução:", solucao_profundidade_cidades)

# print("\nBusca de Custo Uniforme:")
# solucao_custo_uniforme_cidades = busca_custo_uniforme(problema_cidades)
# print("Solução:", solucao_custo_uniforme_cidades)

# print("\nBusca em Profundidade Limitada:")
# solucao_profundidade_limitada = busca_profundidade_limitada(problema_cidades, 3)
# print("Solução:", solucao_profundidade_limitada)

# print("\n\n=== Testando no Grafo Genérico ===")
# print("\nBusca em Largura:")
# solucao_largura_grafo1 = busca_largura(problema_grafo1)
# print("Solução:", solucao_largura_grafo1)

# print("\nBusca em Profundidade:")
# solucao_profundidade_grafo1 = busca_profundidade(problema_grafo1)
# print("Solução:", solucao_profundidade_grafo1)

# print("\nBusca de Custo Uniforme:")
# solucao_custo_uniforme_grafo1 = busca_custo_uniforme(problema_grafo1)
# print("Solução:", solucao_custo_uniforme_grafo1)

print("\nBusca em Profundidade Limitada:")
solucao_profundidade_limitada = busca_profundidade_limitada(problema_grafo1, 3)
print("Solução:", solucao_profundidade_limitada)

