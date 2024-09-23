from problema import Problema, sucessor_grafo, custo_grafo
from algoritmos import busca_largura, busca_profundidade, busca_custo_uniforme, busca_profundidade_limitada

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


# Testando as buscas
print("Busca em Largura:")
solucao_largura_grafo1 = busca_largura(problema_grafo1)
print("Solução:", solucao_largura_grafo1)

print("\nBusca em Profundidade:")
solucao_profundidade_grafo1 = busca_profundidade(problema_grafo1)
print("Solução:", solucao_profundidade_grafo1)

print("\nBusca de Custo Uniforme:")
solucao_custo_uniforme_grafo1 = busca_custo_uniforme(problema_grafo1)
print("Solução:", solucao_custo_uniforme_grafo1)

print("\nBusca em Profundidade Limitada:")
limite = 3
solucao_profundidade_limitada_grafo1 = busca_profundidade_limitada(
    problema_grafo1, limite)
print("Solução:", solucao_profundidade_limitada_grafo1)
