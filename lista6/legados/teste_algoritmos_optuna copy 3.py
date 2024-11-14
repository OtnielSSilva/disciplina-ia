import random
import math
import time
import optuna
import numpy as np
from scipy.stats import kruskal, t
import pandas as pd

# Função de cálculo de conflitos


def calcular_conflitos(tabuleiro):
    conflitos = 0
    n = len(tabuleiro)
    for i in range(n):
        for j in range(i + 1, n):
            if tabuleiro[i] == tabuleiro[j] or abs(tabuleiro[i] - tabuleiro[j]) == abs(i - j):
                conflitos += 1
    return conflitos

# Funções de geração de vizinho para cada algoritmo


def gerar_vizinho_original(tabuleiro):
    n = len(tabuleiro)
    coluna = random.randint(0, n - 1)
    melhor_linha = tabuleiro[coluna]
    menor_conflito = float('inf')
    for linha in range(n):
        if linha != tabuleiro[coluna]:
            novo_tabuleiro = tabuleiro.copy()
            novo_tabuleiro[coluna] = linha
            conflitos = calcular_conflitos(novo_tabuleiro)
            if conflitos < menor_conflito:
                menor_conflito = conflitos
                melhor_linha = linha
    vizinho = tabuleiro.copy()
    vizinho[coluna] = melhor_linha
    return vizinho


def gerar_vizinho_novo(tabuleiro):
    n = len(tabuleiro)
    vizinho = tabuleiro.copy()
    num_movimentos = random.randint(1, 2)
    for _ in range(num_movimentos):
        coluna = random.randint(0, n - 1)
        linha = random.randint(0, n - 1)
        vizinho[coluna] = linha
    return vizinho

# Função de Simulated Annealing


def simulated_annealing(n, temperatura_inicial, resfriamento, vizinho_func):
    temperatura = temperatura_inicial
    limite_iteracoes_sem_melhoria = 5000
    tabuleiro_atual = [random.randint(0, n - 1) for _ in range(n)]
    conflitos_atual = calcular_conflitos(tabuleiro_atual)
    menor_conflito = conflitos_atual
    iteracoes_sem_melhoria = 0
    iteracao = 0

    while conflitos_atual > 0 and temperatura > 0.1:
        tabuleiro_vizinho = vizinho_func(tabuleiro_atual)
        conflitos_vizinho = calcular_conflitos(tabuleiro_vizinho)
        delta = conflitos_vizinho - conflitos_atual

        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperatura):
            tabuleiro_atual = tabuleiro_vizinho
            conflitos_atual = conflitos_vizinho
            if conflitos_atual < menor_conflito:
                menor_conflito = conflitos_atual
                iteracoes_sem_melhoria = 0
            else:
                iteracoes_sem_melhoria += 1
        else:
            iteracoes_sem_melhoria += 1

        if iteracoes_sem_melhoria >= limite_iteracoes_sem_melhoria:
            temperatura = temperatura_inicial
            iteracoes_sem_melhoria = 0

        temperatura *= resfriamento
        iteracao += 1

    return menor_conflito

# Função de otimização com Optuna para ambos os algoritmos


def objective(trial):
    temperatura_inicial = trial.suggest_float("temperatura_inicial", 500, 5000)
    resfriamento = trial.suggest_float("resfriamento", 0.95, 0.999)
    n = 16
    repeticoes = 10
    conflitos_original = []
    conflitos_novo = []
    tempos_original = []
    tempos_novo = []

    for _ in range(repeticoes):
        # Algoritmo original
        start_time = time.time()
        conflitos_original.append(simulated_annealing(
            n, temperatura_inicial, resfriamento, gerar_vizinho_original))
        tempos_original.append(time.time() - start_time)

        # Algoritmo novo
        start_time = time.time()
        conflitos_novo.append(simulated_annealing(
            n, temperatura_inicial, resfriamento, gerar_vizinho_novo))
        tempos_novo.append(time.time() - start_time)

    trial.set_user_attr("conflitos_original", conflitos_original)
    trial.set_user_attr("conflitos_novo", conflitos_novo)
    trial.set_user_attr("tempos_original", tempos_original)
    trial.set_user_attr("tempos_novo", tempos_novo)

    return np.mean(conflitos_original), np.mean(conflitos_novo)


# Otimização com Optuna para ambos os algoritmos
study = optuna.create_study(directions=["minimize", "minimize"])
study.optimize(objective, n_trials=30)

# Coleta dos resultados de conflitos e tempos para análise
conflitos_por_configuracao = []
for trial in study.trials:
    temp_inicial = trial.params["temperatura_inicial"]
    taxa_resfriamento = trial.params["resfriamento"]
    conflitos_original = trial.user_attrs["conflitos_original"]
    conflitos_novo = trial.user_attrs["conflitos_novo"]
    tempos_original = trial.user_attrs["tempos_original"]
    tempos_novo = trial.user_attrs["tempos_novo"]

    def calcula_estatisticas(dados):
        media = np.mean(dados)
        desvio_padrao = np.std(dados, ddof=1)
        t_score = t.ppf(1 - 0.025, df=len(dados) - 1)
        margem_erro = t_score * (desvio_padrao / np.sqrt(len(dados)))
        intervalo_conf = (media - margem_erro, media + margem_erro)
        return media, desvio_padrao, intervalo_conf

    # Estatísticas para conflitos e tempos
    media_conflitos_original, _, intervalo_conflitos_original = calcula_estatisticas(
        conflitos_original)
    media_conflitos_novo, _, intervalo_conflitos_novo = calcula_estatisticas(
        conflitos_novo)
    media_tempo_original, _, intervalo_tempo_original = calcula_estatisticas(
        tempos_original)
    media_tempo_novo, _, intervalo_tempo_novo = calcula_estatisticas(
        tempos_novo)

    conflitos_por_configuracao.append({
        "Temperatura Inicial": temp_inicial,
        "Taxa Resfriamento": taxa_resfriamento,
        "Media Conflitos Original": media_conflitos_original,
        "Intervalo Conflitos Original": intervalo_conflitos_original,
        "Media Tempo Original": media_tempo_original,
        "Intervalo Tempo Original": intervalo_tempo_original,
        "Media Conflitos Novo": media_conflitos_novo,
        "Intervalo Conflitos Novo": intervalo_conflitos_novo,
        "Media Tempo Novo": media_tempo_novo,
        "Intervalo Tempo Novo": intervalo_tempo_novo
    })

# Converte para DataFrame para facilitar a análise
df_conflitos = pd.DataFrame(conflitos_por_configuracao)

# Teste de Kruskal-Wallis para comparar as configurações de conflitos e tempos
grupos_conflitos = [trial.user_attrs["conflitos_original"] +
                    trial.user_attrs["conflitos_novo"] for trial in study.trials]
stat_conflitos, p_value_conflitos = kruskal(*grupos_conflitos)

output = [
    "Melhores Parâmetros dos Trials:\n",
    "\n".join([f"{trial.params}" for trial in study.best_trials]),
    "\nComparação de Conflitos\n",
    f"Estatística Kruskal-Wallis: {stat_conflitos}\n",
    f"Valor-p Conflitos: {p_value_conflitos}\n"
]

if p_value_conflitos < 0.05:
    output.append(
        "Diferença significativa entre os algoritmos para conflitos.\n")
else:
    output.append(
        "Nenhuma diferença significativa entre os algoritmos para conflitos.\n")

# Salva o DataFrame e saída em arquivo
output.append(
    "\nResultados de Conflitos e Tempos de Execução por Configuração:\n")
output.append(df_conflitos.to_string(index=False))

with open("comparacao_algoritmos.txt", "w") as file:
    file.writelines(output)

print("Resultados salvos no arquivo 'comparacao_algoritmos.txt'")
