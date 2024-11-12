import heapq


def heuristica(nodo, objetivo, tipo='manhattan'):
    if tipo == 'manhattan':
        distancia = 0
        for i in range(1, 9):
            xi, yi = divmod(nodo.index(i), 3)
            xg, yg = divmod(objetivo.index(i), 3)
            distancia += abs(xi - xg) + abs(yi - yg)
        return distancia
    elif tipo == 'fora_do_lugar':
        return sum([1 if nodo[i] != objetivo[i] else 0 for i in range(9)])
    else:
        return 0


def gerar_sucessores(estado, estado_pai):
    sucessores = []
    indice_zero = estado.index(0)
    movimentos = []
    if indice_zero % 3 > 0:
        movimentos.append(-1)  # mover para a esquerda
    if indice_zero % 3 < 2:
        movimentos.append(1)   # mover para a direita
    if indice_zero // 3 > 0:
        movimentos.append(-3)  # mover para cima
    if indice_zero // 3 < 2:
        movimentos.append(3)   # mover para baixo
    for movimento in movimentos:
        novo_estado = estado.copy()
        indice_troca = indice_zero + movimento
        novo_estado[indice_zero], novo_estado[indice_troca] = novo_estado[indice_troca], novo_estado[indice_zero]
        if novo_estado != estado_pai:
            sucessores.append(novo_estado)
    return sucessores


def imprimir_estado(estado):
    for i in range(0, 9, 3):
        linha = estado[i:i+3]
        print(linha)
    print()


def busca(estado_inicial, estado_objetivo, algoritmo='gulosa'):
    fronteira = []
    # (prioridade, estado, custo, caminho, estado_pai)
    heapq.heappush(fronteira, (0, estado_inicial, 0, [estado_inicial], None))
    visitados = set()
    explorados = []
    while fronteira:
        prioridade, estado_atual, custo, caminho, estado_pai = heapq.heappop(
            fronteira)
        estado_tupla = tuple(estado_atual)
        if estado_tupla in visitados:
            continue
        visitados.add(estado_tupla)
        explorados.append(estado_atual)

        if estado_atual == estado_objetivo:
            print(f"Custo Total: {custo}")
            print("-----------------")
            print("Caminho:")
            for estado in caminho:
                imprimir_estado(estado)
            print("Explorados:")
            for estado in explorados:
                imprimir_estado(estado)
            print("--------------")
            print("Borda:")
            for item in fronteira:
                estado_borda = item[1]
                imprimir_estado(estado_borda)
            return

        sucessores = gerar_sucessores(
            estado_atual, estado_pai if estado_pai else [])
        for sucessor in sucessores:
            if tuple(sucessor) in visitados:
                continue
            if algoritmo == 'a*':
                g = custo + 1
                h = heuristica(sucessor, estado_objetivo, tipo='manhattan')
                prioridade_sucessor = g + h
            elif algoritmo == 'gulosa':
                h = heuristica(sucessor, estado_objetivo, tipo='manhattan')
                prioridade_sucessor = h
            heapq.heappush(fronteira, (prioridade_sucessor, sucessor,
                           custo+1, caminho + [sucessor], estado_atual))
    print("Falha ao encontrar solução.")


estado_inicial = [3, 1, 2,
                  0, 4, 5,
                  6, 7, 8]

estado_objetivo = [0, 1, 2,
                   3, 4, 5,
                   6, 7, 8]

busca(estado_inicial, estado_objetivo)

# busca(estado_inicial, estado_objetivo, algoritmo='a*')
