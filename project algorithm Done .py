import tkinter as tk
from tkinter import messagebox
import ast
import heapq
import time
import matplotlib.pyplot as plt

# ------------------ Brute Force using DFS ------------------
def brute_force_shortest_paths(graph, start):
    distances = {castle: float('inf') for castle in graph}
    distances[start] = 0

    def dfs(current, current_distance, visited):
        for neighbor, distance in graph.get(current, []):
            if neighbor not in visited:
                new_distance = current_distance + distance
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                dfs(neighbor, new_distance, visited | {neighbor})

    dfs(start, 0, {start})
    return distances

# ------------------ Dijkstra Algorithm (Greedy) ------------------
def dijkstra(graph, start):
    shortest = {node: float('inf') for node in graph}
    shortest[start] = 0
    heap = [(0, start)]

    while heap:
        current_distance, node = heapq.heappop(heap)
        for neighbor, distance_cost in graph.get(node, []):
            new_distance = current_distance + distance_cost
            if new_distance < shortest[neighbor]:
                shortest[neighbor] = new_distance
                heapq.heappush(heap, (new_distance, neighbor))
    return shortest

# ------------------ GUI Functions ------------------
def parse_input():
    try:
        graph = ast.literal_eval(graph_entry.get("1.0", tk.END).strip())
        start = int(start_entry.get())
        return graph, start
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input:\n{e}")
        return None, None

def display_result(result, method, start_time, end_time):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Results using {method} (Shortest Distances):\n\n")
    for castle, distance_val in sorted(result.items()):
        result_text.insert(tk.END, f"Castle {castle}: {distance_val} units\n")
    time_taken = end_time - start_time
    result_text.insert(tk.END, f"\nTime taken to compute: {time_taken:.10f} seconds")
    
    if method == "Brute Force (DFS)":
        complexity_label.config(text="Time Complexity: O(V + E)")
    else:
        complexity_label.config(text="Time Complexity: O((V + E) * logV)")

def draw_gantt_chart(result, method):
    fig, ax = plt.subplots()
    y_pos = 10
    color = 'tab:blue' if method == "Brute Force (DFS)" else 'tab:green'
    
    for castle, distance_val in sorted(result.items()):
        ax.broken_barh([(0, distance_val)], (y_pos, 5), facecolors=color)
        ax.text(distance_val + 0.2, y_pos + 1, f'Castle {castle}', fontsize=9)
        y_pos += 10

    ax.set_xlabel('Distance (units)')
    ax.set_yticks([])
    ax.set_title(f"Gantt Chart - {method} Results (Distances)")
    plt.tight_layout()
    plt.show()

def run_brute_force():
    graph, start = parse_input()
    if graph is None: return
    start_time = time.perf_counter()
    result = brute_force_shortest_paths(graph, start)
    end_time = time.perf_counter()
    display_result(result, "Brute Force (DFS)", start_time, end_time)
    draw_gantt_chart(result, "Brute Force (DFS)")

def run_dijkstra():
    graph, start = parse_input()
    if graph is None: return
    start_time = time.perf_counter()
    result = dijkstra(graph, start)
    end_time = time.perf_counter()
    display_result(result, "Dijkstra (Greedy)", start_time, end_time)
    draw_gantt_chart(result, "Dijkstra (Greedy)")

# ------------------ GUI Setup ------------------
window = tk.Tk()
window.title("The Fastest Messenger - Shortest Path Visualizer")
window.geometry("600x700")
window.configure(bg="#f0f0f0")

tk.Label(window, text="Enter Graph (as dictionary):", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
graph_entry = tk.Text(window, height=5, width=70)
graph_entry.pack()
graph_entry.insert(tk.END, "{0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}")
tk.Label(window, text="Enter Starting Castle:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
start_entry = tk.Entry(window, width=10)
start_entry.pack()
start_entry.insert(0, "0")

tk.Button(window, text="Run Brute Force (DFS)", command=run_brute_force, bg="#FF9800", fg="white", font=("Arial", 12)).pack(pady=10)
tk.Button(window, text="Run Dijkstra (Greedy)", command=run_dijkstra, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

result_text = tk.Text(window, height=15, width=70)
result_text.pack(pady=10)

complexity_label = tk.Label(window, text="", bg="#f0f0f0", font=("Arial", 12, "bold"))
complexity_label.pack(pady=5)

window.mainloop()