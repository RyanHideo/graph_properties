#!/usr/bin/env python3
import matplotlib.pyplot as plt
import math
import tkinter as tk
from tkinter import simpledialog, messagebox


# Classe que representa o grafo (implementado com dicionário de listas de adjacência)
class Graph:
    def __init__(self):
        self.adj = {}  # chave: vértice, valor: lista de tuplas (vértice vizinho, peso)
        self.weighted = False  # indicador se algum peso é diferente de 1

    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = []

    def add_edge(self, u, v, weight=1):
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight))  # grafo não direcionado
        if weight != 1:
            self.weighted = True

    def vertices(self):
        return list(self.adj.keys())

    def num_edges(self):
        return sum(len(neighbors) for neighbors in self.adj.values()) // 2


# Funções de entrada e visualização

def input_graph_manual():
    g = Graph()
    vertices = simpledialog.askstring("Entrada de Vértices",
                                      "Insira os vértices do grafo (separados por espaço):").split()
    if not vertices:
        messagebox.showinfo("Aviso", "Nenhum vértice informado.")
        return g
    vertices_set = set(vertices)
    for v in vertices:
        g.add_vertex(v)

    i = 1
    while True:
        entrada = simpledialog.askstring(f"Aresta {i}",
                                         "Digite a aresta (vértice1 vértice2 [peso]) ou 'fim' para encerrar:")
        if entrada is None or entrada.lower() == 'fim':
            break
        dados = entrada.split()
        if len(dados) < 2:
            messagebox.showerror("Erro", "Entrada inválida! Informe pelo menos dois vértices.")
            continue
        u, v = dados[0], dados[1]
        if u not in vertices_set or v not in vertices_set:
            messagebox.showerror("Erro", "Um dos vértices não foi declarado inicialmente.")
            continue
        peso = 1
        if len(dados) >= 3:
            try:
                peso = float(dados[2])
            except:
                messagebox.showwarning("Aviso", "Peso inválido; usando 1 como padrão.")
        g.add_edge(u, v, peso)
        i += 1
    return g


def select_predefined_graph():
    predefined_graphs = {
        "1": ("Grafo completo K4", ["A", "B", "C", "D"], [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]),
        "2": ("Árvore com 5 vértices", ["1", "2", "3", "4", "5"], [(0, 1), (0, 2), (2, 3), (2, 4)]),
        "3": ("Ciclo com 5 vértices", ["a", "b", "c", "d", "e"], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]),
    }
    options = "\n".join([f"{k} - {v[0]}" for k, v in predefined_graphs.items()])
    option = simpledialog.askstring("Seleção de Grafo", f"Escolha um grafo:\n{options}")

    if option not in predefined_graphs:
        messagebox.showerror("Erro", "Opção inválida!")
        return Graph()

    graph_info = predefined_graphs[option]
    g = Graph()
    for v in graph_info[1]:
        g.add_vertex(v)
    for u, v in graph_info[2]:
        g.add_edge(graph_info[1][u], graph_info[1][v])

    return g


# Função para desenhar o grafo (sem o uso do networkx)
def draw_graph(grafo):
    # Definir a posição dos nós
    vertices = grafo.vertices()
    num_vertices = len(vertices)

    # Disposição circular dos vértices para evitar sobreposição
    radius = 10
    angle = 2 * math.pi / num_vertices
    pos = {}

    for i, v in enumerate(vertices):
        x = radius * math.cos(i * angle)
        y = radius * math.sin(i * angle)
        pos[v] = (x, y)

    # Criar o gráfico
    fig, ax = plt.subplots()

    # Desenhar as arestas
    for u in grafo.adj:
        for (v, weight) in grafo.adj[u]:
            if u < v:  # Para não desenhar arestas duplicadas
                x_values = [pos[u][0], pos[v][0]]
                y_values = [pos[u][1], pos[v][1]]
                ax.plot(x_values, y_values, 'gray', alpha=0.5)
                # Desenhar o peso da aresta
                mid_x = (pos[u][0] + pos[v][0]) / 2
                mid_y = (pos[u][1] + pos[v][1]) / 2
                ax.text(mid_x, mid_y, str(weight), color="red", fontsize=10, ha='center')

    # Desenhar os nós
    for v in vertices:
        ax.plot(pos[v][0], pos[v][1], 'o', color='lightblue', markersize=10)
        ax.text(pos[v][0], pos[v][1], v, fontsize=12, ha='center', va='center', color='black')

    # Ajustes finais no gráfico
    ax.set_aspect('equal')
    ax.axis('off')  # Desligar eixos
    ax.set_title("Visualização do Grafo")

    plt.show()


# Função principal (interface gráfica)
def main():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do tkinter

    while True:
        opcao = simpledialog.askstring("Menu",
                                       "Escolha uma opção:\n1 - Inserir grafo manualmente\n2 - Carregar grafo predefinido\n3 - Sair")
        if opcao == "1":
            grafo = input_graph_manual()
        elif opcao == "2":
            grafo = select_predefined_graph()
        elif opcao == "3":
            messagebox.showinfo("Saindo", "Saindo do programa...")
            break
        else:
            messagebox.showerror("Erro", "Opção inválida!")
            continue

        # Exibe propriedades do grafo
        messagebox.showinfo("Propriedades do Grafo", f"Vértices: {len(grafo.vertices())}, Arestas: {grafo.num_edges()}")

        ver_imagem = messagebox.askyesno("Visualizar Grafo?", "Deseja visualizar o grafo?")
        if ver_imagem:
            draw_graph(grafo)

        if not messagebox.askyesno("Continuar", "Deseja realizar outra operação?"):
            break


if __name__ == '__main__':
    main()
