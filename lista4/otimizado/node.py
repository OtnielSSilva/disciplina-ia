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
