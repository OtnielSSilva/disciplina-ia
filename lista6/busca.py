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
        print(' '.join(str(num) if num != 0 else ' ' for num in linha))
    print("--------")

def busca(estado_inicial, estado_objetivo, algoritmo='gulosa'):
    fronteira = []
    heapq.heappush(fronteira, (0, estado_inicial, 0, [], None))  # (prioridade, estado, custo, caminho, estado_pai)
    visitados = set()
    num_passos = 0
    while fronteira:
        prioridade, estado_atual, custo, caminho, estado_pai = heapq.heappop(fronteira)
        estado_tupla = tuple(estado_atual)
        if estado_tupla in visitados:
            continue
        visitados.add(estado_tupla)
        caminho = caminho + [estado_atual]
        num_passos += 1

        print(f"\nPasso {num_passos} | Custo: {custo} | Prioridade: {prioridade}")
        print("Estado atual:")
        imprimir_estado(estado_atual)

        if estado_atual == estado_objetivo:
            print("Objetivo alcançado!")
            return

        sucessores = gerar_sucessores(estado_atual, estado_pai if estado_pai else [])
        print("Sucessores gerados:")
        sucessor_prioridades = []
        for sucessor in sucessores:
            if algoritmo == 'gulosa':
                h = heuristica(sucessor, estado_objetivo, tipo='manhattan')
                prioridade_sucessor = h
            elif algoritmo == 'a*':
                g = custo + 1
                h = heuristica(sucessor, estado_objetivo, tipo='manhattan')
                prioridade_sucessor = g + h
            sucessor_prioridades.append((prioridade_sucessor, sucessor))
            print(f"Prioridade: {prioridade_sucessor}")
            imprimir_estado(sucessor)
            heapq.heappush(fronteira, (prioridade_sucessor, sucessor, custo+1, caminho, estado_atual))

        # Identificar o sucessor escolhido (com menor prioridade)
        if sucessor_prioridades:
            menor_prioridade, melhor_sucessor = min(sucessor_prioridades, key=lambda x: x[0])
            print("Sucessor escolhido para expansão futura (menor prioridade):")
            print(f"Prioridade: {menor_prioridade}")
            imprimir_estado(melhor_sucessor)

    print("Falha ao encontrar solução.")

estado_inicial = [1, 2, 3,
                  4, 5, 6,
                  7, 8, 0]

estado_objetivo = [0, 1, 2,
                   3, 4, 5,
                   6, 7, 8]

print("Busca Gulosa:")
busca(estado_inicial, estado_objetivo, algoritmo='gulosa')

print("\nBusca A*:")
busca(estado_inicial, estado_objetivo, algoritmo='a*')
