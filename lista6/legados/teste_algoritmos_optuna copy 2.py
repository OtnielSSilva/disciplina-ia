import random
import math
import optuna
from scipy.stats import kruskal, t
import numpy as np
import pandas as pd

# Função de conflito para o problema das N-Rainhas


def conflito(tabuleiro):
    conflitos = 0
    n = len(tabuleiro)
    for i in range(n):
        for j in range(i+1, n):
            if tabuleiro[i] == tabuleiro[j]:
                conflitos += 1
            elif abs(tabuleiro[i] - tabuleiro[j]) == j - i:
                conflitos += 1
    return conflitos

# Geração de um tabuleiro vizinho


def gerar_vizinho(tabuleiro):
    n = len(tabuleiro)
    vizinho = tabuleiro.copy()
    coluna = random.randint(0, n - 1)
    nova_linha = random.randint(0, n - 1)
    vizinho[coluna] = nova_linha
    return vizinho

# Função de Simulated Annealing com parâmetros ajustáveis


def simulated_annealing(n, temperatura_inicial, taxa_resfriamento):
    temperatura = temperatura_inicial
    tabuleiro_atual = [random.randint(0, n - 1) for _ in range(n)]
    conflitos_atual = conflito(tabuleiro_atual)
    melhor_tabuleiro = tabuleiro_atual.copy()
    menor_conflito = conflitos_atual
    iteracao = 0
    max_iteracoes = 10000

    while conflitos_atual > 0 and temperatura > 0.1 and iteracao < max_iteracoes:
        tabuleiro_vizinho = gerar_vizinho(tabuleiro_atual)
        conflitos_vizinho = conflito(tabuleiro_vizinho)
        delta = conflitos_vizinho - conflitos_atual

        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperatura):
            tabuleiro_atual = tabuleiro_vizinho
            conflitos_atual = conflitos_vizinho
            if conflitos_atual < menor_conflito:
                melhor_tabuleiro = tabuleiro_atual.copy()
                menor_conflito = conflitos_atual
        temperatura *= taxa_resfriamento
        iteracao += 1

    return menor_conflito

# Otimização com Optuna para encontrar os melhores parâmetros


def objective(trial):
    temperatura_inicial = trial.suggest_float("temperatura_inicial", 500, 5000)
    taxa_resfriamento = trial.suggest_float("taxa_resfriamento", 0.95, 0.999)
    n = 8  # Número de rainhas
    repeticoes = 30  # Aumentado o número de repetições para maior estabilidade
    conflitos = [simulated_annealing(
        n, temperatura_inicial, taxa_resfriamento) for _ in range(repeticoes)]
    return np.mean(conflitos)


# Executa o estudo de otimização com Optuna
study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=50)

# Armazena os resultados dos conflitos para cada teste, com múltiplas execuções
conflitos_por_configuracao = []
for trial in study.trials:
    temp_inicial = trial.params["temperatura_inicial"]
    taxa_resfriamento = trial.params["taxa_resfriamento"]
    conflitos = [simulated_annealing(
        8, temp_inicial, taxa_resfriamento) for _ in range(10)]
    media_conflitos = np.mean(conflitos)
    desvio_padrao = np.std(conflitos, ddof=1)
    n = len(conflitos)

    # Calcula o intervalo de confiança de 95%
    t_score = t.ppf(1 - 0.025, df=n - 1)
    margem_erro = t_score * (desvio_padrao / np.sqrt(n))
    intervalo_conf = (media_conflitos - margem_erro,
                      media_conflitos + margem_erro)

    conflitos_por_configuracao.append({
        "Temperatura": temp_inicial,
        "Resfriamento": taxa_resfriamento,
        "Media Conflitos": media_conflitos,
        "Desvio Padrao": desvio_padrao,
        "Intervalo de Confiança": intervalo_conf,
        "Conflitos": conflitos  # Agora armazenando a lista de conflitos para o Kruskal-Wallis
    })

# Converte para DataFrame para facilitar análise
df_conflitos = pd.DataFrame(conflitos_por_configuracao)

# Agrupando os resultados de conflitos para o teste Kruskal-Wallis
grupos = [config['Conflitos'] for config in conflitos_por_configuracao]

# Teste estatístico Kruskal-Wallis para verificar variação nos resultados
stat, p_value = kruskal(*grupos)

# Preparando o conteúdo do arquivo de saída
output = [
    f"Melhores Parâmetros: {study.best_params}\n",
    f"Menor número de conflitos encontrado: {study.best_value}\n",
    "\nTeste Kruskal-Wallis\n",
    f"Estatística: {stat}\n",
    f"Valor-p: {p_value}\n",
]

if p_value < 0.05:
    output.append(
        "Diferença estatisticamente significativa entre as configurações.\n")
else:
    output.append(
        "Nenhuma diferença estatisticamente significativa encontrada entre as configurações.\n")

# Adicionando o DataFrame com as configurações e intervalos de confiança
output.append(
    "\nResultados de Conflitos por Configuração com Intervalo de Confiança:\n")
output.append(df_conflitos.to_string(index=False))

# Salvando o resultado no arquivo meta_heuristica.txt
with open("meta_heuristica.txt", "w") as file:
    file.writelines(output)

print("Resultados salvos no arquivo 'meta_heuristica.txt'")
