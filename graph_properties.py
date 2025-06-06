#!/usr/bin/env python3
import matplotlib.pyplot as plt
import networkx as nx  # Usado APENAS para visualização


# Classe que representa o grafo (implementado com dicionário de listas de adjacência)
class Graph:
    def __init__(self):
        self.adj = {}  # chave: vértice, valor: lista de tuplas (vértice vizinho, peso)
        self.weighted = False  # indicador se algum peso é diferente de 1

    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = []

    def add_edge(self, u, v, weight=1):
        # Aqui não criamos vértices automaticamente, eles devem já ter sido declarados
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight))  # grafo não direcionado
        if weight != 1:
            self.weighted = True

    def vertices(self):
        return list(self.adj.keys())

    def num_edges(self):
        # Cada aresta aparece duas vezes na lista de adjacência
        return sum(len(neighbors) for neighbors in self.adj.values()) // 2


# Estrutura de Union-Find (para o algoritmo de Kruskal)
class UnionFind:
    def __init__(self, elements):
        self.parent = {e: e for e in elements}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        rootA = self.find(a)
        rootB = self.find(b)
        self.parent[rootB] = rootA


# --- Funções para calcular as propriedades do grafo (implementadas manualmente) ---

# 1. Conectividade (usando DFS)
def is_connected(graph):
    verts = graph.vertices()
    if not verts:
        return True
    visited = set()
    stack = [verts[0]]
    while stack:
        v = stack.pop()
        if v not in visited:
            visited.add(v)
            for (neighbor, _) in graph.adj[v]:
                if neighbor not in visited:
                    stack.append(neighbor)
    return len(visited) == len(verts)


# 2. Cálculo dos graus de cada vértice, grau máximo e mínimo
def degrees_info(graph):
    degrees = {v: len(graph.adj[v]) for v in graph.vertices()}
    return degrees, max(degrees.values()), min(degrees.values())


# 3. Busca em largura (BFS) para calcular distâncias a partir de um vértice
def bfs(graph, start):
    distances = {v: float('inf') for v in graph.vertices()}
    distances[start] = 0
    queue = [start]
    while queue:
        v = queue.pop(0)
        for (neighbor, _) in graph.adj[v]:
            if distances[neighbor] == float('inf'):
                distances[neighbor] = distances[v] + 1
                queue.append(neighbor)
    return distances


# 4. Cálculo do raio e diâmetro (para grafo conexo)
def radius_diameter(graph):
    ecc = {}  # excentricidade de cada vértice
    for v in graph.vertices():
        dist = bfs(graph, v)
        ecc[v] = max(dist.values())
    return min(ecc.values()), max(ecc.values())


# 5. Algoritmo de Kruskal para encontrar a árvore geradora mínima (MST)
def kruskal_mst(graph):
    edges = []
    # Criamos uma lista de arestas sem duplicatas
    for u in graph.adj:
        for (v, w) in graph.adj[u]:
            if u < v:
                edges.append((w, u, v))
    edges.sort(key=lambda x: x[0])
    uf = UnionFind(graph.vertices())
    mst_edges = []
    total_weight = 0
    for (w, u, v) in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst_edges.append((u, v, w))
            total_weight += w
    return mst_edges, total_weight


# 6. Verifica se o grafo é completo
def is_complete(graph):
    verts = graph.vertices()
    n = len(verts)
    for v in verts:
        if len(graph.adj[v]) != n - 1:
            return False
    return True


# 7. Verifica se o grafo é Euleriano (conexo e todos os vértices com grau par)
def is_eulerian(graph):
    if not is_connected(graph):
        return False
    for v in graph.vertices():
        if len(graph.adj[v]) % 2 != 0:
            return False
    return True


# 8. Busca por ciclo Hamiltoniano (backtracking)
def find_hamiltonian_cycle(graph):
    verts = graph.vertices()
    n = len(verts)
    if n == 0:
        return None
    start = verts[0]
    path = [start]
    visited = {start}

    def backtrack(current):
        if len(path) == n:
            # Verifica se o último vértice tem aresta de volta ao início
            for (neighbor, _) in graph.adj[current]:
                if neighbor == start:
                    return True
            return False
        for (neighbor, _) in graph.adj[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                if backtrack(neighbor):
                    return True
                path.pop()
                visited.remove(neighbor)
        return False

    if backtrack(start):
        path.append(start)
        return path
    else:
        return None


# 9. Verifica se o grafo possui ciclo (usando DFS)
def has_cycle(graph):
    visited = set()

    def dfs(v, parent):
        visited.add(v)
        for (neighbor, _) in graph.adj[v]:
            if neighbor not in visited:
                if dfs(neighbor, v):
                    return True
            elif neighbor != parent:
                return True
        return False

    for v in graph.vertices():
        if v not in visited:
            if dfs(v, None):
                return True
    return False


# 10. Cálculo do número cromático usando backtracking
def chromatic_number_backtracking(graph):
    verts = graph.vertices()
    n = len(verts)
    colors = {v: None for v in verts}
    best_solution = [n + 1]  # inicializa com um valor acima do máximo possível

    def is_valid(v, color):
        for (neighbor, _) in graph.adj[v]:
            if colors[neighbor] == color:
                return False
        return True

    def backtrack(index, max_color_used):
        if index == n:
            best_solution[0] = min(best_solution[0], max_color_used)
            return
        if max_color_used >= best_solution[0]:
            return
        v = verts[index]
        for color in range(max_color_used):
            if is_valid(v, color):
                colors[v] = color
                backtrack(index + 1, max_color_used)
                colors[v] = None
        colors[v] = max_color_used
        backtrack(index + 1, max_color_used + 1)
        colors[v] = None

    backtrack(0, 0)
    return best_solution[0]


# 11. Algoritmo de coloração guloso (pode não ser o ótimo)
def greedy_coloring(graph):
    verts = graph.vertices()
    coloring = {}
    for v in verts:
        neighbor_colors = {coloring.get(neighbor) for (neighbor, _) in graph.adj[v] if neighbor in coloring}
        color = 0
        while color in neighbor_colors:
            color += 1
        coloring[v] = color
    return max(coloring.values()) + 1 if coloring else 0


# --- Funções de entrada e visualização ---

# Entrada manual com validação dos vértices (apenas arestas entre vértices previamente declarados)
def input_graph_manual():
    g = Graph()
    print("=== Inserção Manual de Grafo ===")
    print("1. Insira os vértices do grafo em uma única linha, separados por espaços.")
    print("   Exemplo: A B C D")
    vertices = input("Vértices: ").split()
    if not vertices:
        print("Nenhum vértice informado. Retornando ao menu.")
        return g
    vertices_set = set(vertices)
    for v in vertices:
        g.add_vertex(v)

    print("\n2. Insira as arestas do grafo.")
    print("   Cada aresta deve ser informada no formato:")
    print("      vértice1 vértice2 [peso]")
    print("   - 'vértice1' e 'vértice2' devem ter sido previamente declarados.")
    print("   - Se o peso não for informado, será considerado 1.")
    print("   Digite 'fim' para encerrar.\n")

    i = 1
    while True:
        entrada = input(f"Aresta {i}: ").strip()
        if entrada.lower() == 'fim':
            break
        dados = entrada.split()
        if len(dados) < 2:
            print("Entrada inválida! Informe pelo menos dois vértices.")
            continue
        u, v = dados[0], dados[1]
        if u not in vertices_set or v not in vertices_set:
            print("Entrada inválida! Um dos vértices não foi declarado inicialmente.")
            continue
        peso = 1
        if len(dados) >= 3:
            try:
                peso = float(dados[2])
            except:
                print("Peso inválido; usando 1 como padrão.")
        g.add_edge(u, v, peso)
        i += 1
    return g


# Seleção de grafos predefinidos (exemplos)
def select_predefined_graph():
    print("Selecione um grafo predefinido:")
    print("1 - Grafo completo K4")
    print("2 - Árvore com 5 vértices")
    print("3 - Ciclo com 5 vértices")
    opcao = input("Opção: ")
    g = Graph()
    if opcao == "1":
        vertices = ["A", "B", "C", "D"]
        for v in vertices:
            g.add_vertex(v)
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                g.add_edge(vertices[i], vertices[j])
    elif opcao == "2":
        vertices = ["1", "2", "3", "4", "5"]
        for v in vertices:
            g.add_vertex(v)
        g.add_edge("1", "2")
        g.add_edge("1", "3")
        g.add_edge("3", "4")
        g.add_edge("3", "5")
    elif opcao == "3":
        vertices = ["a", "b", "c", "d", "e"]
        for v in vertices:
            g.add_vertex(v)
        g.add_edge("a", "b")
        g.add_edge("b", "c")
        g.add_edge("c", "d")
        g.add_edge("d", "e")
        g.add_edge("e", "a")
    else:
        print("Opção inválida. Criando grafo vazio.")
    return g


# Função para desenhar o grafo (usando NetworkX apenas para visualização)
def draw_graph(grafo):
    G = nx.Graph()
    for v in grafo.vertices():
        G.add_node(v)
    added_edges = set()
    for u in grafo.adj:
        for (v, weight) in grafo.adj[u]:
            if (v, u) not in added_edges:
                G.add_edge(u, v, weight=weight)
                added_edges.add((u, v))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            edge_color='gray', node_size=800, font_size=10)
    weights = nx.get_edge_attributes(G, 'weight')
    if any(w != 1 for w in weights.values()):
        nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
    plt.title("Visualização do Grafo")
    plt.show()


# --- Função principal (menu) ---
def main():
    while True:
        print("\n=== Programa de Propriedades de Grafos ===")
        print("1 - Inserir grafo manualmente")
        print("2 - Carregar grafo predefinido")
        print("3 - Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            grafo = input_graph_manual()
        elif opcao == "2":
            grafo = select_predefined_graph()
        elif opcao == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")
            continue

        # Exibindo propriedades do grafo (calculadas sem NetworkX)
        print("\n=== Propriedades do Grafo ===")
        print("Número de vértices:", len(grafo.vertices()))
        print("Número de arestas:", grafo.num_edges())

        graus, grau_max, grau_min = degrees_info(grafo)
        print("Graus dos vértices:", graus)
        print("Grau máximo:", grau_max)
        print("Grau mínimo:", grau_min)

        conexo = is_connected(grafo)
        print("Grafo conexo:", "Sim" if conexo else "Não")

        if conexo:
            raio, diametro = radius_diameter(grafo)
            print("Raio:", raio)
            print("Diâmetro:", diametro)
        else:
            print("Raio e diâmetro não podem ser calculados em grafos desconexos.")

        if grafo.weighted and conexo:
            mst, peso_total = kruskal_mst(grafo)
            print("Árvore Geradora Mínima (arestas e pesos):")
            for (u, v, w) in mst:
                print(f"  {u} - {v} (peso: {w})")
            print("Peso total do MST:", peso_total)
        else:
            print("Grafo não é ponderado ou não é conexo; MST não aplicável.")

        ciclo = has_cycle(grafo)
        print("Grafo acíclico:", "Sim" if not ciclo else "Não")

        completo = is_complete(grafo)
        print("Grafo completo:", "Sim" if completo else "Não")

        euleriano = is_eulerian(grafo)
        print("Grafo Euleriano:", "Sim" if euleriano else "Não")

        if len(grafo.vertices()) > 10:
            print("Verificação de ciclo Hamiltoniano ignorada para grafos com mais de 10 vértices.")
        else:
            hamiltoniano = find_hamiltonian_cycle(grafo)
            if hamiltoniano:
                print("Ciclo Hamiltoniano encontrado:", " -> ".join(hamiltoniano))
            else:
                print("Grafo não possui ciclo Hamiltoniano.")

        if len(grafo.vertices()) <= 10:
            nc = chromatic_number_backtracking(grafo)
            print("Número cromático (backtracking):", nc)
        else:
            nc = greedy_coloring(grafo)
            print("Número cromático (algoritmo guloso):", nc)

        print("Perímetro: Propriedade não implementada (definição ambígua em grafos).")

        ver_imagem = input("\nDeseja visualizar o grafo? (s/n): ")
        if ver_imagem.lower() == "s":
            draw_graph(grafo)

        input("\nPressione Enter para voltar ao menu...")


if __name__ == '__main__':
    main()
