import tkinter as tk
from tkinter import ttk
from collections import deque
import heapq

class Problema:
    def __init__(self, estado_inicial, estado_objetivo, grafo):
        self.estado_inicial = estado_inicial
        self.estado_objetivo = estado_objetivo
        self.grafo = grafo

    def objetivo_alcancado(self, estado):
        return estado == self.estado_objetivo

    def expandir(self, estado):
        return self.grafo[estado]  # Retorna tanto o estado quanto o custo da aresta

# Busca em Largura (BFS)
def busca_em_largura(problema, output_text):
    borda = deque([problema.estado_inicial])  # Fila para a busca em largura
    explorado = set()
    caminho = {problema.estado_inicial: None}  # Para reconstruir o caminho
    passos = 0  # Contador de passos

    while borda:
        no = borda.popleft()
        if no in explorado:
            continue
        explorado.add(no)
        passos += 1

        output_text.insert(tk.END, f"Passo {passos}: Explorando {no}\n")
        output_text.insert(tk.END, f"Borda atual: {list(borda)}\n\n")
        output_text.update_idletasks()

        if problema.objetivo_alcancado(no):
            output_text.insert(tk.END, f"Nós expandidos: {len(explorado)}\n")
            return reconstruir_caminho(caminho, problema.estado_inicial, no, explorado, borda, output_text)

        for vizinho, _ in problema.expandir(no):
            if vizinho not in explorado and vizinho not in borda:
                borda.append(vizinho)
                caminho[vizinho] = no

    output_text.insert(tk.END, "Falha: solução não encontrada\n")
    return None

# Busca em Profundidade (DFS)
def busca_em_profundidade(problema, output_text):
    borda = deque([problema.estado_inicial])  # Pilha para a busca em profundidade
    explorado = set()
    caminho = {problema.estado_inicial: None}  # Para reconstruir o caminho
    passos = 0

    while borda:
        no = borda.pop()
        if no in explorado:
            continue
        explorado.add(no)
        passos += 1

        output_text.insert(tk.END, f"Passo {passos}: Explorando {no}\n")
        output_text.insert(tk.END, f"Borda atual: {list(borda)}\n\n")
        output_text.update_idletasks()

        if problema.objetivo_alcancado(no):
            output_text.insert(tk.END, f"Nós expandidos: {len(explorado)}\n")
            return reconstruir_caminho(caminho, problema.estado_inicial, no, explorado, borda, output_text)

        for vizinho, _ in problema.expandir(no):
            if vizinho not in explorado and vizinho not in borda:
                borda.append(vizinho)
                caminho[vizinho] = no

    output_text.insert(tk.END, "Falha: solução não encontrada\n")
    return None

# Busca de Custo Uniforme (Uniform Cost Search)
def busca_de_custo_uniforme(problema, output_text):
    borda = []
    heapq.heappush(borda, (0, problema.estado_inicial))  # Fila de prioridade para a busca de custo uniforme
    explorado = set()
    caminho = {problema.estado_inicial: None}  # Para reconstruir o caminho
    custo = {problema.estado_inicial: 0}
    passos = 0

    while borda:
        custo_atual, no = heapq.heappop(borda)
        if no in explorado:
            continue
        explorado.add(no)
        passos += 1

        output_text.insert(tk.END, f"Passo {passos}: Explorando {no} com custo {custo_atual}\n")
        output_text.insert(tk.END, f"Borda atual: {[(c, n) for c, n in borda]}\n\n")
        output_text.update_idletasks()  # Atualizar a interface imediatamente

        if problema.objetivo_alcancado(no):
            output_text.insert(tk.END, f"Custo total da solução: {custo_atual}\n")
            output_text.insert(tk.END, f"Nós expandidos: {len(explorado)}\n")
            output_text.update_idletasks()  # Atualizar a interface imediatamente
            return reconstruir_caminho(caminho, problema.estado_inicial, no, explorado, borda, output_text)

        for vizinho, custo_vizinho in problema.expandir(no):
            novo_custo = custo_atual + custo_vizinho  # Usando o custo fornecido
            if vizinho not in explorado and (vizinho not in custo or novo_custo < custo[vizinho]):
                custo[vizinho] = novo_custo
                heapq.heappush(borda, (novo_custo, vizinho))
                caminho[vizinho] = no

    output_text.insert(tk.END, "Falha: solução não encontrada\n")
    output_text.update_idletasks()  # Atualizar a interface imediatamente
    return None

# Função para reconstruir o caminho encontrado
def reconstruir_caminho(caminho, inicio, fim, explorado, borda, output_text):
    percurso = []
    while fim:
        percurso.append(fim)
        fim = caminho[fim]
    percurso.reverse()

    output_text.insert(tk.END, f"\nCaminho encontrado: {percurso}\n")
    output_text.insert(tk.END, f"Nós explorados: {sorted(explorado)}\n")
    output_text.insert(tk.END, f"Borda final: {list(borda)}\n")
    output_text.insert(tk.END, f"Total de nós explorados: {len(explorado)}\n")
    return percurso

# Função para iniciar a busca e atualizar a interface gráfica
def iniciar_busca():
    output_text.delete(1.0, tk.END)
    estado_inicial = entrada_inicial.get()
    estado_objetivo = entrada_objetivo.get()
    tipo_busca = busca_var.get()
    grafo_selecionado = grafo_var.get()

    if grafo_selecionado == "Romênia":
        grafo = grafo_romenia
    else:
        grafo = grafo_personalizado

    nos_validos = list(grafo.keys())
    if not estado_inicial or not estado_objetivo:
        output_text.insert(tk.END, "Erro: Por favor, selecione o nó inicial e o nó objetivo.\n")
        return

    if estado_inicial not in nos_validos or estado_objetivo not in nos_validos:
        output_text.insert(tk.END, "Erro: Nó inicial ou objetivo inválido para o grafo selecionado.\n")
        return

    problema = Problema(estado_inicial=estado_inicial, estado_objetivo=estado_objetivo, grafo=grafo)

    if tipo_busca == "Largura":
        busca_em_largura(problema, output_text)
    elif tipo_busca == "Profundidade":
        busca_em_profundidade(problema, output_text)
    elif tipo_busca == "Custo Uniforme":
        busca_de_custo_uniforme(problema, output_text)

# Função para atualizar os nós disponíveis nos Comboboxes quando o grafo selecionado muda
def atualizar_nos(*args):
    grafo_selecionado = grafo_var.get()
    if grafo_selecionado == "Romênia":
        grafo = grafo_romenia
    else:
        grafo = grafo_personalizado
    nos = list(grafo.keys())
    entrada_inicial['values'] = nos
    entrada_objetivo['values'] = nos
    entrada_inicial.set('')  # Limpar seleção atual
    entrada_objetivo.set('')  # Limpar seleção atual

# Definindo o mapa da Romênia como grafo com os custos
grafo_romenia = {
    'Arad': [('Sibiu', 140), ('Timisoara', 118), ('Zerind', 75)],
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
    'Craiova': [('Drobeta', 120), ('Pitesti', 138), ('Rimnicu Vilcea', 146)],
    'Bucareste': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu': [('Bucareste', 90)],
    'Urziceni': [('Bucareste', 85), ('Vaslui', 142), ('Hirsova', 98)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)]
}

# Definindo o grafo personalizado com os custos
grafo_personalizado = {
    'A': [('B', 3), ('C', 1), ('D', 2)],
    'B': [('A', 3), ('D', 3), ('E', 3)],
    'C': [('A', 1), ('D', 2), ('G', 0)],
    'D': [('A', 2), ('B', 3), ('C', 2), ('E', 3), ('F', 4), ('G', 0)],
    'E': [('B', 3), ('D', 3), ('F', 4)],
    'F': [('D', 4), ('E', 4), ('G', 5)],
    'G': [('C', 0), ('D', 0), ('F', 5)]
}

# Interface gráfica usando tkinter
root = tk.Tk()
root.title("Algoritmos de Busca - Mapa da Romênia e Grafo Personalizado")

# Frame para o grafo
frame_grafo = tk.LabelFrame(root, text="Selecione o Grafo")
frame_grafo.pack(pady=10, padx=10, fill="x")

# Seleção do grafo
grafo_var = tk.StringVar(value="Romênia")
grafo_romenia_rb = tk.Radiobutton(frame_grafo, text="Romênia", variable=grafo_var, value="Romênia", command=atualizar_nos)
grafo_personalizado_rb = tk.Radiobutton(frame_grafo, text="Personalizado", variable=grafo_var, value="Personalizado", command=atualizar_nos)
grafo_romenia_rb.pack(side="left", padx=5, pady=5)
grafo_personalizado_rb.pack(side="left", padx=5, pady=5)

# Seleção do tipo de busca
frame_busca = tk.LabelFrame(root, text="Selecione o Tipo de Busca")
frame_busca.pack(pady=10, padx=10, fill="x")

busca_var = tk.StringVar(value="Largura")
busca_largura_rb = tk.Radiobutton(frame_busca, text="Largura", variable=busca_var, value="Largura")
busca_profundidade_rb = tk.Radiobutton(frame_busca, text="Profundidade", variable=busca_var, value="Profundidade")
busca_custo_uniforme_rb = tk.Radiobutton(frame_busca, text="Custo Uniforme", variable=busca_var, value="Custo Uniforme")

busca_largura_rb.pack(side="left", padx=5, pady=5)
busca_profundidade_rb.pack(side="left", padx=5, pady=5)
busca_custo_uniforme_rb.pack(side="left", padx=5, pady=5)

# Frame para a entrada dos nós
frame_entrada = tk.Frame(root)
frame_entrada.pack(pady=10, padx=10)

# Entrada para o nó inicial
tk.Label(frame_entrada, text="Nó Inicial:").grid(row=0, column=0, padx=5, pady=5)
entrada_inicial = ttk.Combobox(frame_entrada, state='readonly')
entrada_inicial.grid(row=0, column=1, padx=5, pady=5)

# Entrada para o nó objetivo
tk.Label(frame_entrada, text="Nó Objetivo:").grid(row=1, column=0, padx=5, pady=5)
entrada_objetivo = ttk.Combobox(frame_entrada, state='readonly')
entrada_objetivo.grid(row=1, column=1, padx=5, pady=5)

# Botão para iniciar a busca
buscar_button = tk.Button(root, text="Iniciar Busca", command=iniciar_busca)
buscar_button.pack(pady=10)

# Frame para conter o Text widget e o Scrollbar
frame_output = tk.Frame(root)
frame_output.pack(pady=10, padx=10, expand=True, fill='both')

# Scrollbar
scrollbar = tk.Scrollbar(frame_output)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Texto para exibir os resultados
output_text = tk.Text(frame_output, height=20, width=80, yscrollcommand=scrollbar.set)
output_text.pack(pady=10, padx=10, expand=True, fill='both')

# Associar o Scrollbar ao Text widget
scrollbar.config(command=output_text.yview)

# Configurar fonte para o Text widget
import tkinter.font as tkFont
font = tkFont.Font(family="Helvetica", size=10)
output_text.configure(font=font)

# Inicializar os nós nos Comboboxes
atualizar_nos()

# Rodar a interface gráfica
root.mainloop()
