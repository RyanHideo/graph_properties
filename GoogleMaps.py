import networkx as nx
import matplotlib.pyplot as plt
import heapq

# Criar o grafo
G = nx.Graph()

# Adicionar as arestas (vértices ligados e pesos)
edges = [
    ('A', 'B', 4),
    ('A', 'C', 2),
    ('B', 'C', 1),
    ('B', 'D', 5),
    ('C', 'D', 8),
    ('C', 'E', 10),
    ('D', 'E', 2),
    ('D', 'Z', 6),
    ('E', 'Z', 3)
]

for edge in edges:
    u, v, weight = edge
    G.add_edge(u, v, weight=weight)

# Função Dijkstra para encontrar o menor caminho
def dijkstra(graph, start, end):
    queue = []
    heapq.heappush(queue, (0, start))

    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0

    previous_nodes = {node: None for node in graph.nodes}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]['weight']
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path.reverse()

    return path, distances[end]

# Entrada do usuário
print("Nós disponíveis:", list(G.nodes))
start_node = input("Digite o nó de partida: ").strip()
end_node = input("Digite o nó de chegada: ").strip()

# Verificar se os nós são válidos
if start_node not in G.nodes or end_node not in G.nodes:
    print("Erro: Um dos nós digitados não existe no grafo.")
else:
    path, cost = dijkstra(G, start_node, end_node)
    print(f"\nMenor caminho de {start_node} até {end_node}: {' -> '.join(path)}")
    print(f"Custo total: {cost}")

    # Layout fixo
    pos = {
        'A': (0, 2),
        'B': (2, 2),
        'C': (1, 3),
        'D': (2, 1),
        'E': (1, 0),
        'Z': (3, 0)
    }

    plt.figure(figsize=(8,6))

    # Desenhar o grafo completo
    # Cores dos nós: amarelo para os do caminho, azul claro para os demais
    node_colors = ['yellow' if node in path else 'lightblue' for node in G.nodes]

    # Desenhar nós com as cores definidas
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=10)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Destacar o menor caminho em vermelho
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)

    plt.title(f"Menor caminho de {start_node} até {end_node}")
    plt.axis('off')  # tira os eixos x e y
    plt.show()
