import numpy as np
from scipy.stats import kruskal, mannwhitneyu
import scikit_posthocs as sp
from statsmodels.stats.proportion import proportions_ztest
import time

# Importe suas funções principais de busca e meta-heurística
from busca import busca
from meta_heuristica import simulated_annealing

# Configurações dos testes
num_execucoes = 50
resultados_busca = []
resultados_meta_heuristica = []

estado_inicial = [3, 1, 2, 0, 4, 5, 6, 7, 8]
estado_objetivo = [0, 1, 2, 3, 4, 5, 6, 7, 8]

# Executa os testes para ambos os algoritmos
for _ in range(num_execucoes):
    # Teste para o algoritmo de busca
    start_time = time.time()
    busca(estado_inicial, estado_objetivo, algoritmo='a*')
    tempo_busca = time.time() - start_time
    resultados_busca.append(tempo_busca)

    # Teste para o Simulated Annealing
    start_time = time.time()
    simulated_annealing(8)
    tempo_sa = time.time() - start_time
    resultados_meta_heuristica.append(tempo_sa)

# Converte os resultados para arrays
resultados_busca = np.array(resultados_busca)
resultados_meta_heuristica = np.array(resultados_meta_heuristica)

# Teste Kruskal-Wallis
stat, p_value = kruskal(resultados_busca, resultados_meta_heuristica)
print(f"Kruskal-Wallis: Estatística H = {stat}, p-valor = {p_value}")

# Teste de Nemenyi
dados = np.array([resultados_busca, resultados_meta_heuristica]).T
nemenyi_results = sp.posthoc_nemenyi_friedman(dados)
print("Resultados do Teste de Nemenyi:\n", nemenyi_results)

# Teste de Proporção - Verifique se há sucessos
sucessos_busca = sum(1 for x in resultados_busca if x == 0)
sucessos_sa = sum(1 for x in resultados_meta_heuristica if x == 0)

if sucessos_busca > 0 or sucessos_sa > 0:
    n_busca = len(resultados_busca)
    n_sa = len(resultados_meta_heuristica)
    stat, p_value = proportions_ztest(
        [sucessos_busca, sucessos_sa], [n_busca, n_sa])
    print(f"Teste de Proporção: Estatística Z = {stat}, p-valor = {p_value}")
else:
    print("Nenhum dos algoritmos encontrou uma solução ótima, teste de proporção não aplicado.")

# Teste de Mann-Whitney como alternativa ao Friedman para dois conjuntos
stat, p_value = mannwhitneyu(resultados_busca, resultados_meta_heuristica)
print(f"Mann-Whitney: Estatística = {stat}, p-valor = {p_value}")
