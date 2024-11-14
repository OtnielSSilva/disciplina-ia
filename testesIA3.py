import numpy as np
import random
from scipy.stats import kruskal
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Parâmetros gerais
N_QUEENS = 16
MAX_FITNESS = int(N_QUEENS * (N_QUEENS - 1) / 2)  # Número máximo de pares não conflitantes

# Função para criar um indivíduo (permutação dos números de 0 a N-1)
def create_individual(n):
    return random.sample(range(n), n)

# Função para criar uma população inicial
def create_population(pop_size, n):
    return [create_individual(n) for _ in range(pop_size)]

# Função de fitness (avalia o número de pares não conflitantes)
def fitness(individual):
    n = len(individual)
    diag1 = [individual[i] + i for i in range(n)]
    diag2 = [individual[i] - i for i in range(n)]
    conflicts = (n - len(set(diag1))) + (n - len(set(diag2)))
    return MAX_FITNESS - conflicts

# Busca Genética 1 (heurística melhor)
def genetic_algorithm_1(pop_size, generations):
    mutation_rate = 0.1
    population = create_population(pop_size, N_QUEENS)
    best_fitness = float('-inf')
    fitness_history = []

    for gen in range(generations):
        fitnesses = [fitness(ind) for ind in population]
        fitness_history.append({
            'generation': gen,
            'mean_fitness': np.mean(fitnesses),
            'std_fitness': np.std(fitnesses)
        })
        new_population = []

        for _ in range(pop_size):
            # Seleção por torneio
            participants = random.sample(population, 3)
            parent1 = max(participants, key=fitness)
            participants = random.sample(population, 3)
            parent2 = max(participants, key=fitness)

            # Crossover uniforme
            child = [parent1[i] if random.random() > 0.5 else parent2[i] for i in range(N_QUEENS)]
            # Corrigir duplicatas e ausências
            child = repair_individual(child)

            # Mutação
            if random.random() < mutation_rate:
                child = swap_mutation(child)

            new_population.append(child)

        population = new_population
        current_best_fitness = max(fitnesses)
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness

    return best_fitness, fitness_history

# Busca Genética 2 (heurística pior)
def genetic_algorithm_2(pop_size, generations):
    mutation_rate = 0.01
    population = create_population(pop_size, N_QUEENS)
    best_fitness = float('-inf')
    fitness_history = []

    for gen in range(generations):
        fitnesses = [fitness(ind) for ind in population]
        fitness_history.append({
            'generation': gen,
            'mean_fitness': np.mean(fitnesses),
            'std_fitness': np.std(fitnesses)
        })
        new_population = []

        for _ in range(pop_size):
            # Seleção aleatória
            parent1 = random.choice(population)
            parent2 = random.choice(population)

            # Crossover de um ponto
            crossover_point = random.randint(1, N_QUEENS - 1)
            child = parent1[:crossover_point] + parent2[crossover_point:]
            # Corrigir duplicatas e ausências
            child = repair_individual(child)

            # Mutação
            if random.random() < mutation_rate:
                child = swap_mutation(child)

            new_population.append(child)

        population = new_population
        current_best_fitness = max(fitnesses)
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness

    return best_fitness, fitness_history

# Busca Genética 4 (Seu Algoritmo)
def genetic_algorithm_4(pop_size, generations):
    mutation_rate = 0.05
    population = create_population(pop_size, N_QUEENS)
    best_fitness = float('-inf')
    fitness_history = []

    for gen in range(generations):
        fitnesses = [fitness(ind) for ind in population]
        total_fitness = sum(fitnesses)
        if total_fitness == 0:
            probabilities = [1/len(fitnesses)] * len(fitnesses)
        else:
            probabilities = [f / total_fitness for f in fitnesses]
        fitness_history.append({
            'generation': gen,
            'mean_fitness': np.mean(fitnesses),
            'std_fitness': np.std(fitnesses)
        })
        new_population = []

        for _ in range(pop_size):
            # Seleção por roleta
            parent1 = population[np.random.choice(range(pop_size), p=probabilities)]
            parent2 = population[np.random.choice(range(pop_size), p=probabilities)]

            # Cruzamento de Ordem (Order Crossover - OX)
            child = order_crossover(parent1, parent2)

            # Mutação
            if random.random() < mutation_rate:
                child = swap_mutation(child)

            new_population.append(child)

        population = new_population
        current_best_fitness = max(fitnesses)
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness

    return best_fitness, fitness_history

# Funções auxiliares
def repair_individual(individual):
    """Repara um indivíduo que possa ter duplicatas ou ausências."""
    n = len(individual)
    missing = list(set(range(n)) - set(individual))
    counts = {}
    duplicates = []
    for idx, gene in enumerate(individual):
        counts[gene] = counts.get(gene, 0) + 1
        if counts[gene] > 1:
            duplicates.append(idx)
    for idx in duplicates:
        individual[idx] = missing.pop()
    return individual

def swap_mutation(individual):
    """Mutação por troca de posição entre dois genes."""
    idx1, idx2 = random.sample(range(len(individual)), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

def order_crossover(parent1, parent2):
    """Cruzamento de Ordem (Order Crossover - OX)."""
    n = len(parent1)
    start, end = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[start:end] = parent1[start:end]
    pos = end % n
    for gene in parent2[end:] + parent2[:end]:
        if gene not in child:
            child[pos] = gene
            pos = (pos + 1) % n
    return child

# Função para simular o ajuste de hiperparâmetros
def hyperparameter_tuning(ga_function, iterations, pop_size, generations):
    results = []
    fitness_histories = []
    for _ in range(iterations):
        fitness_value, fitness_history = ga_function(pop_size, generations)
        results.append(fitness_value)
        fitness_histories.append(fitness_history)
    return results, fitness_histories

# Variáveis globais para armazenar os últimos resultados
last_results_ga1 = []
last_results_ga2 = []
last_results_ga4 = []
last_histories_ga1 = []
last_histories_ga2 = []
last_histories_ga4 = []

# Função para exibir o dashboard
def show_dashboard():
    if not last_results_ga1 or not last_results_ga2 or not last_results_ga4:
        messagebox.showerror("Erro", "Por favor, execute os testes primeiro.")
        return

    dashboard_window = tk.Toplevel(root)
    dashboard_window.title("Dashboard de Comparação")
    dashboard_window.configure(bg='#F0F0F0')  # Fundo suave

    # Criar um DataFrame com os resultados
    data = {
        'Busca Genética 1': last_results_ga1,
        'Busca Genética 2': last_results_ga2,
        'Seu Algoritmo': last_results_ga4
    }
    df_results = pd.DataFrame(data)

    # Estatísticas descritivas
    stats = df_results.describe().T

    # Configurar o layout com uma figura maior e ajustada
    fig = plt.figure(figsize=(14, 12))

    # Boxplot com médias e intervalos de confiança (primeira linha, coluna 1)
    ax1 = fig.add_subplot(3, 2, 1)
    ax1.boxplot([last_results_ga1, last_results_ga2, last_results_ga4],
                labels=['Busca Genética 1', 'Busca Genética 2', 'Seu Algoritmo'],
                showmeans=True)
    ax1.set_title('Boxplot dos Resultados de Fitness')
    ax1.set_ylabel('Fitness')

    # Histograma (primeira linha, coluna 2)
    ax2 = fig.add_subplot(3, 2, 2)
    ax2.hist([last_results_ga1, last_results_ga2, last_results_ga4],
             label=['GA1', 'GA2', 'Seu Algoritmo'], bins=10, alpha=0.7)
    ax2.set_title('Histograma dos Resultados de Fitness')
    ax2.set_xlabel('Fitness')
    ax2.set_ylabel('Frequência')
    ax2.legend()

    # Estatísticas descritivas detalhadas (segunda linha, ocupando toda a largura)
    ax3 = fig.add_subplot(3, 1, 2)
    ax3.axis('off')
    table = ax3.table(cellText=np.round(stats.values, 4),
                      rowLabels=stats.index,
                      colLabels=stats.columns,
                      loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)  # Aumenta o tamanho da tabela
    ax3.set_title('Estatísticas Descritivas')

    # Gráfico de Convergência por Geração (terceira linha, ocupando toda a largura)
    ax4 = fig.add_subplot(3, 1, 3)
    generations = range(int(generations_entry.get()))
    mean_history_ga1 = np.mean([[h['mean_fitness'] for h in hist] for hist in last_histories_ga1], axis=0)
    mean_history_ga2 = np.mean([[h['mean_fitness'] for h in hist] for hist in last_histories_ga2], axis=0)
    mean_history_ga4 = np.mean([[h['mean_fitness'] for h in hist] for hist in last_histories_ga4], axis=0)

    ax4.plot(generations, mean_history_ga1, label='GA1')
    ax4.plot(generations, mean_history_ga2, label='GA2')
    ax4.plot(generations, mean_history_ga4, label='Seu Algoritmo')
    ax4.set_title('Convergência Média por Geração')
    ax4.set_xlabel('Geração')
    ax4.set_ylabel('Fitness Médio')
    ax4.legend()

    # Ajustar o layout
    plt.tight_layout()

    # Adicionar o canvas à janela Tkinter
    canvas = FigureCanvasTkAgg(fig, master=dashboard_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Função para exibir a explicação de como analisar os resultados
def show_analysis_explanation():
    # Criar uma nova janela para a explicação
    analysis_window = tk.Toplevel(root)
    analysis_window.title("Como Analisar os Resultados")
    analysis_window.configure(bg='#F0F0F0')  # Fundo suave

    # Definir a fonte personalizada
    heading_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
    subtitle_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
    body_font = tkfont.Font(family="Helvetica", size=12)

    # Frame principal
    main_frame = tk.Frame(analysis_window, bg='#F0F0F0', padx=10, pady=10)
    main_frame.pack(expand=True, fill='both')

    # Canvas para a barra de rolagem
    canvas = tk.Canvas(main_frame, bg='#F0F0F0')
    canvas.pack(side='left', fill='both', expand=True)

    scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')

    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame interno
    content_frame = tk.Frame(canvas, bg='#F0F0F0')
    canvas.create_window((0, 0), window=content_frame, anchor='nw')

    # Atualizar a região de rolagem
    content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Inserir o texto da explicação
    explanation = """
Como Analisar os Resultados:

- **Média de Fitness**: Indica o desempenho médio de cada busca genética. Valores mais altos são melhores.

- **Boxplot**: Visualiza a distribuição dos resultados de fitness. Observe a mediana, quartis e possíveis outliers.

- **Histograma**: Mostra a frequência dos valores de fitness obtidos. Ajuda a entender a distribuição dos resultados.

- **Gráfico de Convergência**: Exibe a evolução do fitness médio ao longo das gerações. Permite comparar a taxa de convergência dos algoritmos.

- **Estatísticas Descritivas**: Inclui média, mediana, desvio padrão, valores mínimo e máximo, e quartis.

- **Outliers**: Valores atípicos que podem indicar execuções anômalas do algoritmo. Importante analisar separadamente.

- **Teste Kruskal-Wallis**:
   - Estatística H: Mede a diferença entre as distribuições dos grupos.
   - Valor-p: Se for menor que 0,05, indica uma diferença estatisticamente significativa.

**Interpretação**:

- Compare as médias de fitness para entender o desempenho geral.
- Use o boxplot e o histograma para visualizar a variabilidade e consistência dos resultados.
- Observe o gráfico de convergência para ver qual algoritmo converge mais rapidamente.
- Considere o valor-p para determinar se as diferenças observadas são significativas ou podem ser atribuídas ao acaso.
"""

    # Criar um Label para o texto
    explanation_label = tk.Label(content_frame, text=explanation, justify='left', bg='#F0F0F0', fg='#000000', font=body_font)
    explanation_label.pack(expand=True, fill='both')

# Função para exibir a explicação das diferenças
def show_explanation():
    # Criar uma nova janela para a explicação
    explanation_window = tk.Toplevel(root)
    explanation_window.title("Explicação das Diferenças")
    explanation_window.configure(bg='#F0F0F0')  # Fundo suave

    # Definir a fonte personalizada
    heading_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
    subtitle_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
    body_font = tkfont.Font(family="Helvetica", size=12)

    # Frame principal
    main_frame = tk.Frame(explanation_window, bg='#F0F0F0', padx=10, pady=10)
    main_frame.pack(expand=True, fill='both')

    # Canvas para a barra de rolagem
    canvas = tk.Canvas(main_frame, bg='#F0F0F0')
    canvas.pack(side='left', fill='both', expand=True)

    scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')

    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame interno
    content_frame = tk.Frame(canvas, bg='#F0F0F0')
    canvas.create_window((0, 0), window=content_frame, anchor='nw')

    # Atualizar a região de rolagem
    content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Inserir o texto da explicação
    explanation = """
Diferenças entre as Buscas Genéticas:

**Busca Genética 1 (Heurística Melhor):**
- Seleção por Torneio: Seleciona os melhores indivíduos de um grupo aleatório.
- Crossover Uniforme: Cada gene do filho tem 50% de chance de vir de cada pai.
- Alta Taxa de Mutação (10%): Promove maior diversidade genética.

**Busca Genética 2 (Heurística Pior):**
- Seleção Aleatória: Pais são selecionados aleatoriamente sem considerar aptidão.
- Crossover de Um Ponto: Troca genes após um ponto escolhido aleatoriamente.
- Baixa Taxa de Mutação (1%): Menor diversidade genética.

**Seu Algoritmo:**
- Seleção por Roleta: Probabilidade de seleção proporcional à aptidão.
- Cruzamento de Ordem (OX): Preserva a ordem relativa dos genes.
- Taxa de Mutação Moderada (5%): Equilíbrio entre exploração e explotação.
"""

    # Criar um Label para o texto
    explanation_label = tk.Label(content_frame, text=explanation, justify='left', bg='#F0F0F0', fg='#000000', font=body_font)
    explanation_label.pack(expand=True, fill='both')

# Função para exibir a explicação do fitness
def show_fitness_explanation():
    # Criar uma nova janela para a explicação
    fitness_window = tk.Toplevel(root)
    fitness_window.title("Explicação do Fitness")
    fitness_window.configure(bg='#F0F0F0')  # Fundo suave

    # Definir a fonte personalizada
    heading_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
    subtitle_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
    body_font = tkfont.Font(family="Helvetica", size=12)

    # Frame principal
    main_frame = tk.Frame(fitness_window, bg='#F0F0F0', padx=10, pady=10)
    main_frame.pack(expand=True, fill='both')

    # Canvas para a barra de rolagem
    canvas = tk.Canvas(main_frame, bg='#F0F0F0')
    canvas.pack(side='left', fill='both', expand=True)

    scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')

    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame interno
    content_frame = tk.Frame(canvas, bg='#F0F0F0')
    canvas.create_window((0, 0), window=content_frame, anchor='nw')

    # Atualizar a região de rolagem
    content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Inserir o texto da explicação
    explanation = """
Explicação do Cálculo de Fitness e Importância:

**Cálculo de Fitness**:
- O fitness avalia a qualidade de uma solução contando o número de pares de rainhas que **não estão em conflito**.
- Como as rainhas são posicionadas em linhas e colunas únicas (devido à representação), os conflitos possíveis são nas **diagonais**.
- Diagonais principais e secundárias são calculadas, e conflitos são identificados se mais de uma rainha estiver na mesma diagonal.
- O fitness é calculado como `MAX_FITNESS - conflitos`, onde `MAX_FITNESS` é o número máximo de pares não conflitantes.
- **Maior fitness** indica **menos conflitos** e uma solução melhor.

**Por que Algoritmos com Maior Média de Fitness são Melhores**:
- Uma média de fitness mais alta significa que, em geral, o algoritmo produz soluções com **menos conflitos**.
- Isso reflete a **eficácia do algoritmo** em encontrar soluções de alta qualidade.
- Não está diretamente relacionado ao tempo de execução, mas sim à **qualidade das soluções** geradas.
- Algoritmos com maior média de fitness são mais **eficientes na exploração** do espaço de busca para o problema das N-Rainhas.

**Conclusão**:
- Avaliar o fitness permite comparar o desempenho dos algoritmos em termos da qualidade das soluções encontradas.
- Algoritmos que consistentemente produzem soluções com fitness mais alto são considerados melhores para resolver o problema.
"""

    # Criar um Label para o texto
    explanation_label = tk.Label(content_frame, text=explanation, justify='left', bg='#F0F0F0', fg='#000000', font=body_font)
    explanation_label.pack(expand=True, fill='both')

# Função para executar os testes e exibir os resultados
def run_tests():
    try:
        iterations = int(iterations_entry.get())
        pop_size = int(pop_size_entry.get())
        generations = int(generations_entry.get())

        if iterations <= 0 or pop_size <= 0 or generations <= 0:
            raise ValueError

        results_ga1, histories_ga1 = hyperparameter_tuning(genetic_algorithm_1, iterations, pop_size, generations)
        results_ga2, histories_ga2 = hyperparameter_tuning(genetic_algorithm_2, iterations, pop_size, generations)
        results_ga4, histories_ga4 = hyperparameter_tuning(genetic_algorithm_4, iterations, pop_size, generations)

        # Armazenar os resultados em variáveis globais
        global last_results_ga1, last_results_ga2, last_results_ga4
        global last_histories_ga1, last_histories_ga2, last_histories_ga4
        last_results_ga1 = results_ga1
        last_results_ga2 = results_ga2
        last_results_ga4 = results_ga4
        last_histories_ga1 = histories_ga1
        last_histories_ga2 = histories_ga2
        last_histories_ga4 = histories_ga4

        # Teste estatístico não paramétrico (Kruskal-Wallis)
        stat, p_value = kruskal(results_ga1, results_ga2, results_ga4)

        # Formatação dos resultados para exibição mais clara
        formatted_results_ga1 = [f"{result:.4f}" for result in results_ga1]
        formatted_results_ga2 = [f"{result:.4f}" for result in results_ga2]
        formatted_results_ga4 = [f"{result:.4f}" for result in results_ga4]

        result_text = "Resultados da Comparação entre as Buscas Genéticas:\n\n"
        result_text += "Busca Genética 1 (Melhor Heurística):\n"
        result_text += f" - Resultados: {formatted_results_ga1}\n"
        result_text += f" - Média de Fitness: {np.mean(results_ga1):.4f}\n\n"

        result_text += "Busca Genética 2 (Pior Heurística):\n"
        result_text += f" - Resultados: {formatted_results_ga2}\n"
        result_text += f" - Média de Fitness: {np.mean(results_ga2):.4f}\n\n"

        result_text += "Seu Algoritmo:\n"
        result_text += f" - Resultados: {formatted_results_ga4}\n"
        result_text += f" - Média de Fitness: {np.mean(results_ga4):.4f}\n\n"

        result_text += "Teste Kruskal-Wallis entre os algoritmos:\n"
        result_text += f" - Estatística H: {stat:.2f}\n"
        result_text += f" - Valor-p: {p_value:.4e}\n\n"

        if p_value < 0.05:
            conclusion = "Conclusão: Há diferenças estatisticamente significativas entre os algoritmos."
        else:
            conclusion = "Conclusão: Não há diferenças estatisticamente significativas entre os algoritmos."

        result_text += conclusion

        result_label.config(text=result_text)

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores inteiros positivos para as entradas.")

# Interface Gráfica
root = tk.Tk()
root.title("Comparação de Buscas Genéticas")
root.configure(bg='#F0F0F0')  # Fundo suave

# Definir fonte padrão para os widgets
default_font = tkfont.Font(family="Helvetica", size=12)
title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")

# Estilo para os botões
button_style = {'font': default_font, 'bg': '#ADD8E6', 'activebackground': '#87CEEB'}

# Título principal
title_label = tk.Label(root, text="Comparação de Buscas Genéticas", font=title_font, bg='#F0F0F0')
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Entrada para o número de iterações
iterations_label = tk.Label(root, text="Número de Iterações:", font=default_font, bg='#F0F0F0')
iterations_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
iterations_entry = tk.Entry(root, font=default_font)
iterations_entry.grid(row=1, column=1, padx=5, pady=5)
iterations_entry.insert(0, "5")

# Entrada para o tamanho da população
pop_size_label = tk.Label(root, text="Tamanho da População:", font=default_font, bg='#F0F0F0')
pop_size_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')
pop_size_entry = tk.Entry(root, font=default_font)
pop_size_entry.grid(row=2, column=1, padx=5, pady=5)
pop_size_entry.insert(0, "100")

# Entrada para o número de gerações
generations_label = tk.Label(root, text="Número de Gerações:", font=default_font, bg='#F0F0F0')
generations_label.grid(row=3, column=0, padx=5, pady=5, sticky='e')
generations_entry = tk.Entry(root, font=default_font)
generations_entry.grid(row=3, column=1, padx=5, pady=5)
generations_entry.insert(0, "50")

# Botão para executar os testes
run_button = tk.Button(root, text="Executar Testes", command=run_tests, **button_style)
run_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

# Label para exibir os resultados
result_label = tk.Label(root, text="", justify="left", font=default_font, bg='#F0F0F0')
result_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Botão para exibir a explicação das diferenças
explanation_button = tk.Button(root, text="Explicação das Diferenças", command=show_explanation, **button_style)
explanation_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

# Botão para exibir o dashboard
dashboard_button = tk.Button(root, text="Mostrar Dashboard", command=show_dashboard, **button_style)
dashboard_button.grid(row=7, column=0, columnspan=2, padx=5, pady=10)

# Botão para explicar como analisar os resultados
analysis_button = tk.Button(root, text="Como Analisar os Resultados", command=show_analysis_explanation, **button_style)
analysis_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10)

# Botão para explicar o cálculo do fitness
fitness_button = tk.Button(root, text="Explicação do Fitness", command=show_fitness_explanation, **button_style)
fitness_button.grid(row=9, column=0, columnspan=2, padx=5, pady=10)

root.mainloop()
