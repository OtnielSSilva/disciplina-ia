from problema import Problema, sucessor_grafo, custo_grafo
from algoritmos import busca_largura, busca_profundidade, busca_custo_uniforme, busca_profundidade_limitada

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

# Testando as buscas
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
