import tkinter as tk
from tkinter import simpledialog, messagebox
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def dijkstra(graph, start, goal):
    shortest_paths = {vertex: (float('infinity'), None) for vertex in graph}
    shortest_paths[start] = (0, None)
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        if current_vertex == goal:
            break
        
        if current_distance > shortest_paths[current_vertex][0]:
            continue
        
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < shortest_paths[neighbor][0]:
                shortest_paths[neighbor] = (distance, current_vertex)
                heapq.heappush(priority_queue, (distance, neighbor))
    
    path = []
    while goal is not None:
        path.insert(0, goal)
        goal = shortest_paths[goal][1]
    
    if not path or path[0] != start:
        raise Exception("Caminho não encontrado ou inválido!")
    
    return path, shortest_paths

def plot_graph(graph, path, start_router, goal_router, canvas):
    G = nx.Graph()
    
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)
    
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=12, font_weight='bold', edge_color='gray')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red')
    nx.draw_networkx_edges(G, pos, edgelist=[(path[i], path[i+1]) for i in range(len(path)-1)], edge_color='red', width=2.5)
    plt.title(f'dijkstra de {start_router} para {goal_router}')
    
    canvas.figure.clear()
    ax = canvas.figure.add_subplot(111)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=12, font_weight='bold', edge_color='gray', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red', ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=[(path[i], path[i+1]) for i in range(len(path)-1)], edge_color='red', width=2.5, ax=ax)
    ax.set_title(f'dijkstra de {start_router} para {goal_router}')
    canvas.draw()

class GraphEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Editor de Grafo")
        self.geometry("800x600")
        
        self.graph = {
            'A': {'B': 2, 'C': 4, 'D': 7},
            'B': {'A': 2, 'C': 1, 'E': 5},
            'C': {'A': 4, 'B': 1, 'D': 3, 'F': 6},
            'D': {'A': 7, 'C': 3, 'G': 2},
            'E': {'B': 5, 'F': 3},
            'F': {'C': 6, 'E': 3, 'G': 1},
            'G': {'D': 2, 'F': 1}
        }


        self.start_router = 'A'
        self.goal_router = 'G'

        self.create_widgets()

    def create_widgets(self):
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.figure = plt.Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.update_plot()
        
        self.control_frame = tk.Frame(self)
        self.control_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.control_frame.columnconfigure(0, weight=1)
        self.control_frame.columnconfigure(1, weight=1)
        self.control_frame.columnconfigure(2, weight=1)
        self.control_frame.columnconfigure(3, weight=1)
        self.control_frame.columnconfigure(4, weight=1)

        tk.Button(self.control_frame, text="Adicionar Aresta", command=self.add_edge).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.control_frame, text="Remover Aresta", command=self.remove_edge).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.control_frame, text="Adicionar Nó", command=self.add_node).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(self.control_frame, text="Remover Nó", command=self.remove_node).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(self.control_frame, text="Calcular Caminho", command=self.calculate_path).grid(row=0, column=4, padx=5, pady=5)
        tk.Button(self.control_frame, text="Sair", command=self.quit).grid(row=1, column=0, columnspan=5, padx=5, pady=5)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

    def update_plot(self):
        try:
            path, _ = dijkstra(self.graph, self.start_router, self.goal_router)
            plot_graph(self.graph, path, self.start_router, self.goal_router, self.canvas)
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def add_edge(self):
        node1 = simpledialog.askstring("Adicionar Aresta", "Nó de origem:")
        node2 = simpledialog.askstring("Adicionar Aresta", "Nó de destino:")
        weight = simpledialog.askinteger("Adicionar Aresta", "Peso da aresta:")
        
        if node1 and node2 and weight is not None:
            if node1 not in self.graph:
                self.graph[node1] = {}
            if node2 not in self.graph:
                self.graph[node2] = {}
            self.graph[node1][node2] = weight
            self.graph[node2][node1] = weight
            self.update_plot()

    def remove_edge(self):
        node1 = simpledialog.askstring("Remover Aresta", "Nó de origem:")
        node2 = simpledialog.askstring("Remover Aresta", "Nó de destino:")
        
        if node1 in self.graph and node2 in self.graph:
            if node2 in self.graph[node1]:
                del self.graph[node1][node2]
            if node1 in self.graph[node2]:
                del self.graph[node2][node1]
            self.update_plot()
    
    def add_node(self):
        node = simpledialog.askstring("Adicionar Nó", "Nome do nó:")
        
        if node:
            if node not in self.graph:
                self.graph[node] = {}
            self.update_plot()

    def remove_node(self):
        node = simpledialog.askstring("Remover Nó", "Nome do nó:")
        
        if node in self.graph:
            del self.graph[node]
            for n in self.graph:
                if node in self.graph[n]:
                    del self.graph[n][node]
            self.update_plot()

    def calculate_path(self):
        start = simpledialog.askstring("Caminho Mais Curto", "Nó de início:")
        goal = simpledialog.askstring("Caminho Mais Curto", "Nó de destino:")
        
        if start and goal:
            self.start_router = start
            self.goal_router = goal
            self.update_plot()

if __name__ == "__main__":
    app = GraphEditor()
    app.mainloop()
