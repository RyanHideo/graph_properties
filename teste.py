import networkx as nx
import matplotlib.pyplot as plt


def encontrar_menor_caminho(grafo, origem, destino):
    """
    Encontra o menor caminho entre dois pontos usando o algoritmo de Dijkstra.

    :param grafo: Grafo NetworkX
    :param origem: Nó de origem
    :param destino: Nó de destino
    :return: Menor caminho e distância total
    """
    caminho = nx.dijkstra_path(grafo, origem, destino, weight='weight')
    distancia = nx.dijkstra_path_length(grafo, origem, destino, weight='weight')
    return caminho, distancia


def desenhar_grafo(grafo, caminho=None):
    """
    Desenha o grafo e destaca o menor caminho se fornecido.

    :param grafo: Grafo NetworkX
    :param caminho: Lista de nós representando o menor caminho
    """
    pos = nx.spring_layout(grafo)  # Layout para posicionamento dos nós
    labels = nx.get_edge_attributes(grafo, 'weight')

    plt.figure(figsize=(8, 6))
    nx.draw(grafo, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1500, font_size=10)
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels)

    if caminho:
        caminho_edges = list(zip(caminho, caminho[1:]))
        nx.draw_networkx_edges(grafo, pos, edgelist=caminho_edges, edge_color='red', width=2)

    plt.show()


# Criando o grafo
G = nx.Graph()
arestas = [
    ('A', 'B', 6), ('A', 'C', 4), ('B', 'C', 7),
    ('B', 'D', 10), ('C', 'D', 5), ('D', 'E', 3),
    ('E', 'A', 7), ('E', 'B', 5)
]

# Adicionando as arestas ao grafo
for u, v, w in arestas:
    G.add_edge(u, v, weight=w)

# Definir os pontos de origem e destino
origem = 'A'
destino = 'D'

# Encontrar o menor caminho
caminho, distancia = encontrar_menor_caminho(G, origem, destino)

# Exibir os resultados
print(f"Menor caminho de {origem} para {destino}: {caminho} com distância {distancia}")

# Desenhar o grafo com o menor caminho destacado
desenhar_grafo(G, caminho)
