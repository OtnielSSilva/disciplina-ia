from collections import deque
import heapq
from node import Node, solucao, expandir

# Modifique o algoritmo para que essa estratégia dimunua a quantidade de nós armazenados na BORDA.


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
            print(f"Custo total da solução: {no.custo}")
            print(f"Quantidade de nós expandidos: {len(nos_expandidos_list)}")
            print(f"Número de nós na BORDA final: {len(borda_final)}")
            # print(f"Nos na BORDA final: {[n.estado for n in borda_final]}")
            # print(f"Todos os nós adicionados na BORDA: {todos_nos_na_borda}")
            # print(f"Todos os nós expandidos: {nos_expandidos_list}")
            return solucao(no)

        explorados.add(no.estado)

        for filho in expandir(no, problema):
            if filho.estado not in explorados and filho.estado not in estados_na_borda:
                borda.append(filho)
                estados_na_borda.add(filho.estado)
                todos_nos_na_borda.append(filho.estado)

    return None

# É possível encontrar alguma solução mais barata que essa ? É possível encontrar alguma solução que exija menos passos até a solução (sequência de ações ou cidades visitadas no caminho entre a origem e destino) ?


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
            print(f"Custo total da solução: {no.custo}")
            print(f"Quantidade de nós expandidos: {len(nos_expandidos_list)}")
            print(f"Número de nós na BORDA final: {len(borda_final)}")
            # print(f"Nos na BORDA final: {[n.estado for n in borda_final]}")
            # print(f"Todos os nós adicionados na BORDA: {todos_nos_na_borda}")
            # print(f"Todos os nós expandidos: {nos_expandidos_list}")
            return solucao(no)

        explorados.add(no.estado)

        # Reverso para manter a ordem correta na pilha
        for filho in reversed(expandir(no, problema)):
            if filho.estado not in explorados and filho.estado not in estados_na_borda:
                borda.append(filho)
                estados_na_borda.add(filho.estado)
                todos_nos_na_borda.append(filho.estado)

    return None

# Modifique o algoritmo para que essa estratégia dimunua a quantidade de nós armazenados na BORDA


def busca_custo_uniforme(problema):
    borda = []
    heapq.heappush(borda, (0, Node(problema.estado_inicial)))
    explorados = {}

    # Listas para armazenar os nós para impressão
    todos_nos_na_borda = []
    nos_expandidos_list = []

    while borda:
        custo_atual, no = heapq.heappop(borda)
        nos_expandidos_list.append(no.estado)

        if problema.estado_objetivo(no.estado):
            borda_final = [n for c, n in borda]
            borda_final_estados = [n.estado for n in borda_final]
            print(f"Custo total da solução: {no.custo}")
            print(f"Quantidade de nós expandidos: {len(nos_expandidos_list)}")
            print(f"Número de nós na BORDA final: {len(borda_final_estados)}")
            # print(f"Nos na BORDA final: {borda_final_estados}")
            # print(f"Todos os nós adicionados na BORDA: {todos_nos_na_borda}")
            # print(f"Todos os nós expandidos: {nos_expandidos_list}")
            return solucao(no)

        if no.estado not in explorados or custo_atual < explorados[no.estado]:
            explorados[no.estado] = custo_atual
            for sucessor in expandir(no, problema):
                if sucessor.estado not in explorados or sucessor.custo < explorados.get(sucessor.estado, float('inf')):
                    heapq.heappush(borda, (sucessor.custo, sucessor))
                    todos_nos_na_borda.append(sucessor.estado)

    return None


def busca_profundidade_limitada(problema, limite):
    nos_expandidos = set()
    nos_armazenados = set()

    def recursive_dls(no, problema, limite):
        # Adiciona o estado do nó atual aos nós expandidos após a expansão
        if no.estado not in nos_expandidos:
            nos_expandidos.add(no.estado)

        # Verifica se é o estado objetivo
        if problema.estado_objetivo(no.estado):
            return solucao(no), False  # False indica que não houve corte

        # Verifica se atingiu o limite de profundidade
        elif limite == 0:
            return None, True  # True indica corte (CUT-OFF)

        else:
            cutoff_occurred = False
            # Expande os sucessores do nó atual
            for filho in expandir(no, problema):
                if filho.estado not in nos_expandidos:
                    # Adiciona o estado do sucessor nos nós armazenados
                    nos_armazenados.add(filho.estado)
                    resultado, cutoff = recursive_dls(
                        filho, problema, limite - 1)

                    if cutoff:
                        cutoff_occurred = True
                    elif resultado is not None:
                        return resultado, False

            # Se todos os sucessores resultarem em corte, retorna o corte
            return None, cutoff_occurred

    # Inicializa a busca com o estado inicial
    no_inicial = Node(problema.estado_inicial)
    resultado, cutoff = recursive_dls(no_inicial, problema, limite)

    # Relatórios finais sobre a execução da busca
    print(f"Quantidade de nós expandidos: {len(nos_expandidos)}")
    print(f"Quantidade de nós armazenados: {len(nos_armazenados)}")

    if resultado:
        return resultado
    elif cutoff:
        print("Corte ocorreu, solução não encontrada dentro do limite.")
        return None
    else:
        print("Falha, solução não encontrada.")
        return None
