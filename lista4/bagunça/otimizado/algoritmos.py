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


# Busca em Largura com impressão passo a passo
def busca_largura(problema):
    borda = deque([Node(problema.estado_inicial)])
    explorados = set()
    estados_na_borda = set([problema.estado_inicial])

    passos = 0
    print("=== Iniciando Busca em Largura ===\n")

    while borda:
        passos += 1
        print(f"Passo {passos}:")
        print(f"Borda atual: {[n.estado for n in borda]}")

        no = borda.popleft()
        estados_na_borda.remove(no.estado)

        print(f"Explorando nó: {no.estado} (Custo acumulado: {no.custo})")

        if problema.estado_objetivo(no.estado):
            print("\n=== Objetivo Encontrado ===")
            print(f"Custo total da solução: {no.custo}")
            print(f"Quantidade de nós expandidos: {passos}")
            print(f"Número de nós na BORDA final: {len(borda)}")
            print(f"Borda final: {[n.estado for n in borda]}")
            return solucao(no)

        explorados.add(no.estado)

        for filho in expandir(no, problema):
            if filho.estado not in explorados and filho.estado not in estados_na_borda:
                borda.append(filho)
                estados_na_borda.add(filho.estado)
                print(
                    f"Adicionado à borda: {filho.estado} (Custo: {filho.custo})")

        print("")  # Linha em branco para melhor leitura

    print("Falha: solução não encontrada\n")
    return None


# Busca em Profundidade com impressão passo a passo
def busca_profundidade(problema):
    borda = [Node(problema.estado_inicial)]
    explorados = set()
    estados_na_borda = set([problema.estado_inicial])

    passos = 0
    print("=== Iniciando Busca em Profundidade ===\n")

    while borda:
        passos += 1
        print(f"Passo {passos}:")
        print(f"Borda atual: {[n.estado for n in borda]}")

        no = borda.pop()
        estados_na_borda.remove(no.estado)

        print(f"Explorando nó: {no.estado} (Custo acumulado: {no.custo})")

        if problema.estado_objetivo(no.estado):
            print("\n=== Objetivo Encontrado ===")
            print(f"Custo total da solução: {no.custo}")
            print(f"Quantidade de nós expandidos: {passos}")
            print(f"Número de nós na BORDA final: {len(borda)}")
            print(f"Borda final: {[n.estado for n in borda]}")
            return solucao(no)

        explorados.add(no.estado)

        for filho in reversed(expandir(no, problema)):
            if filho.estado not in explorados and filho.estado not in estados_na_borda:
                borda.append(filho)
                estados_na_borda.add(filho.estado)
                print(
                    f"Adicionado à borda: {filho.estado} (Custo: {filho.custo})")

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
        print(f"Borda atual: {[(c, n.estado) for c, n in borda]}")

        custo_atual, no = heapq.heappop(borda)

        print(f"Explorando nó: {no.estado} (Custo acumulado: {custo_atual})")

        if problema.estado_objetivo(no.estado):
            print("\n=== Objetivo Encontrado ===")
            print(f"Custo total da solução: {custo_atual}")
            print(f"Quantidade de nós expandidos: {passos}")
            print(f"Número de nós na BORDA final: {len(borda)}")
            print(f"Borda final: {[n.estado for n in borda]}")
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

        print("")  # Linha em branco para melhor leitura

    print("Falha: solução não encontrada\n")
    return None


# Busca em Profundidade Limitada com impressão passo a passo
def busca_profundidade_limitada(problema, limite):
    nos_expandidos = set()
    passos = 0

    print(
        f"=== Iniciando Busca em Profundidade Limitada (Limite: {limite}) ===\n")

    def recursive_dls(no, problema, limite):
        nonlocal passos
        passos += 1
        print(f"Passo {passos}:")
        print(f"Explorando nó: {no.estado} (Profundidade: {no.profundidade})")

        nos_expandidos.add(no.estado)

        if problema.estado_objetivo(no.estado):
            print("\n=== Objetivo Encontrado ===")
            print(f"Custo total da solução: {no.custo}")
            print(f"Quantidade de nós expandidos: {len(nos_expandidos)}")
            return solucao(no), False

        elif limite == 0:
            print(f"Nó {no.estado} atingiu o limite de profundidade.\n")
            return None, True

        else:
            cutoff_occurred = False
            for filho in expandir(no, problema):
                if filho.estado not in nos_expandidos:
                    resultado, cutoff = recursive_dls(
                        filho, problema, limite - 1)
                    if cutoff:
                        cutoff_occurred = True
                    elif resultado is not None:
                        return resultado, False
            return None, cutoff_occurred

    no_inicial = Node(problema.estado_inicial)
    resultado, cutoff = recursive_dls(no_inicial, problema, limite)

    print(f"Quantidade de nós expandidos: {len(nos_expandidos)}")

    if resultado:
        return resultado
    elif cutoff:
        print("Corte ocorreu, solução não encontrada dentro do limite.\n")
        return None
    else:
        print("Falha, solução não encontrada.\n")
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
