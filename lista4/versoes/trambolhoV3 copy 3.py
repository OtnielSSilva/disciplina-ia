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
    explorados = []
    # Removido estados_na_borda para permitir repetições na borda

    passos = 0
    print("=== Iniciando Busca em Largura ===\n")

    while borda:
        no = borda.popleft()
        
        if no.estado in explorados:
            print(f"Estado {no.estado} já foi explorado, pulando...\n")            
            continue

        passos += 1
        print(f"Passo {passos}:")

        print(f"Explorando nó: {no.estado} (Custo acumulado: {no.custo})")
        explorados.append(no.estado)

        if problema.estado_objetivo(no.estado):
            print("\n=== Objetivo Encontrado ===")
            print(f"Custo total da solução: {no.custo}")
            print(f"Quantidade de nós expandidos: {passos}")
            print(f"Número de nós na BORDA final: {len(borda)}")
            print(f"Borda final: {[n.estado for n in borda]}")
            print(f"Nós explorados: {explorados}")
            # return solucao(no)
            return

        for filho in expandir(no, problema):
            # Adicionando nós repetidos à borda
            borda.append(filho)
            print(f"Adicionado à borda: {filho.estado}")
            # print(f"Adicionado à borda: {filho.estado} (Custo: {filho.custo})")


        print(f"Borda atual: {[n.estado for n in borda]}")
        print("")  # Linha em branco para melhor leitura

    print("Falha: solução não encontrada\n")
    return None


def busca_profundidade(problema):
    borda = [Node(problema.estado_inicial)]
    explorados = []
    # Removido estados_na_borda para permitir repetições na borda

    passos = 0
    print("=== Iniciando Busca em Profundidade ===\n")

    while borda:
        no = borda.pop()  # Remove o último elemento da borda (pilha)

        if no.estado in explorados:
            print(f"Estado {no.estado} já foi explorado, pulando...\n")            
            continue

        passos += 1
        print(f"Passo {passos}:")

        print(f"Explorando nó: {no.estado} (Custo acumulado: {no.custo})")
        explorados.append(no.estado)

        if problema.estado_objetivo(no.estado):
            print("\n=== Objetivo Encontrado ===")
            print(f"Custo total da solução: {no.custo}")
            print(f"Quantidade de nós expandidos: {passos}")
            print(f"Número de nós na BORDA final: {len(borda)}")
            print(f"Borda final: {[n.estado for n in borda]}")
            print(f"Nós explorados: {explorados}")
            return solucao(no)

        # Obter os filhos
        filhos = expandir(no, problema)

        # Adicionar os filhos à borda na ordem inversa manualmente
        # Para explorar D antes de F, adicione F primeiro e depois D
        for filho in filhos:
                borda.append(filho)
                print(
                    f"Adicionado à borda: {filho.estado} (Custo: {filho.custo})")
                
        print(f"Borda atual: {[n.estado for n in borda]}")
        print("")  # Linha em branco para melhor leitura

    print("Falha: solução não encontrada\n")
    return None


# Busca de Custo Uniforme com impressão passo a passo
def busca_custo_uniforme(problema):
    borda = []
    heapq.heappush(borda, (0, Node(problema.estado_inicial)))
    explorados = {}
    estados_na_borda = {problema.estado_inicial: 0}

    passos = 0
    print("=== Iniciando Busca de Custo Uniforme ===\n")

    while borda:
        passos += 1
        print(f"Passo {passos}:")

        custo_atual, no = heapq.heappop(borda)

        print(f"Explorando nó: {no.estado} (Custo acumulado: {custo_atual})")

        if problema.estado_objetivo(no.estado):
            print("\n=== Objetivo Encontrado ===")
            print(f"Custo total da solução: {custo_atual}")
            print(f"Quantidade de nós expandidos: {passos}")
            print(f"Número de nós na BORDA final: {len(borda)}")
            print(f"Borda final: {[n.estado for c, n in borda]}")
            print(f"Nós explorados: {explorados.keys()}")
            return solucao(no)

        explorados[no.estado] = custo_atual
        for sucessor in expandir(no, problema):
            estado_sucessor = sucessor.estado
            custo_sucessor = sucessor.custo

            if estado_sucessor not in explorados or custo_sucessor < explorados.get(estado_sucessor, float('inf')):
                heapq.heappush(borda, (custo_sucessor, sucessor))
                estados_na_borda[estado_sucessor] = custo_sucessor
                print(
                    f"Adicionado à borda: {sucessor.estado} (Custo: {sucessor.custo})")

        print(f"Borda atual: {[(c, n.estado) for c, n in borda]}")
        print("")  # Linha em branco para melhor leitura

    print("Falha: solução não encontrada\n")
    return None


# Definição do grafo das cidades
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