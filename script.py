import heapq
import networkx as nx
import sys

def build_graph(file_name):
    G = nx.DiGraph()
    with open(file_name, 'r') as file:
        for line in file:
            data = line.split()
            node1, node2, weight = data[0], data[1], float(data[2])
            G.add_edge(node1, node2, weight=weight)
            G.add_edge(node2, node1, weight=weight)  # Adding the reverse edge
    return G


def add_edge(graph, tail, head, transmit_time):
    graph.add_edge(tail, head, weight=transmit_time)
    graph.add_edge(head, tail, weight=transmit_time)

def delete_edge(graph, tail, head):
    if graph.has_edge(tail, head):
        graph.remove_edge(tail, head)
        graph.remove_edge(head, tail)

def edge_down(graph, tail, head):
    if graph.has_edge(tail, head):
        graph[tail][head]['down'] = True

def edge_up(graph, tail_vertex, head_vertex):
    if tail_vertex in graph and head_vertex in graph[tail_vertex]:
        graph[tail_vertex][head_vertex].pop('down', None)
        return True
    elif head_vertex in graph and tail_vertex in graph[head_vertex]:
        graph[head_vertex][tail_vertex].pop('down', None)
        return True
    return False

def vertex_down(graph, vertex):
    if graph.has_node(vertex):
        graph.nodes[vertex]['down'] = True

def vertex_up(graph, vertex):
    if vertex in graph.nodes():
        graph.nodes[vertex].pop('down', None)
        return True
    return False


def dijkstra(graph, start, end):
    pq = []  # Priority queue for Dijkstra's algorithm
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    heapq.heappush(pq, (0, start))

    while pq:
        current_dist, current_node = heapq.heappop(pq)
        if current_node == end:
            break

        if current_dist > distances[current_node]:
            continue

        for neighbor, edge_data in graph[current_node].items():
            if 'down' in edge_data or 'down' in graph.nodes[current_node]:
                continue  # Skip edges or vertices marked as "down"

            neighbor_dist = current_dist + edge_data.get('weight', float('inf'))
            if neighbor_dist < distances[neighbor]:
                distances[neighbor] = neighbor_dist
                heapq.heappush(pq, (neighbor_dist, neighbor))

    path = [end]
    while end != start:
        for predecessor in graph.predecessors(end):
            if distances[end] == distances[predecessor] + graph[predecessor][end].get('weight', float('inf')):
                path.append(predecessor)
                end = predecessor
                break

    path.reverse()
    return path, round(distances[path[-1]], 2) if path[-1] != start else 0



def print_graph(graph):
    for node in sorted(graph.nodes()):
        edges = sorted(graph[node].items(), key=lambda x: x[0])
        if 'down' in graph.nodes[node]:
            print(f"{node} DOWN")
        else:
            print(node)
        for neighbor, data in edges:
            if 'down' in data:
                print(f"{neighbor} {data['weight']} DOWN")
            else:
                print(f"{neighbor} {data['weight']}")

def reachable_vertices(graph):
    reachable = {}

    def dfs(node, visited, reachable_set):
        visited.add(node)
        reachable_set.add(node)
        for neighbor, data in graph[node].items():
            if neighbor != node and 'down' not in data and 'down' not in graph.nodes[neighbor] and neighbor not in visited:
                dfs(neighbor, visited, reachable_set)

    for node in graph.nodes():
        if 'down' not in graph.nodes[node]:
            visited = set()
            reachable_set = set()
            dfs(node, visited, reachable_set)
            reachable[node] = sorted(reachable_set - {node})

    return reachable



def process_query(graph, query):
    query_data = query.split()
    command = query_data[0]

    if command == "addedge":
        tail, head, transmit_time = query_data[1], query_data[2], float(query_data[3])
        add_edge(graph, tail, head, transmit_time)
    elif command == "deleteedge":
        tail, head = query_data[1], query_data[2]
        delete_edge(graph, tail, head)
    elif command == "edgedown":
        tail, head = query_data[1], query_data[2]
        edge_down(graph, tail, head)
    elif command == "edgeup":
        tail, head = query_data[1], query_data[2]
        edge_up(graph, tail, head)
    elif command == "vertexdown":
        vertex = query_data[1]
        vertex_down(graph, vertex)
    elif command == "vertexup":
        vertex = query_data[1]
        vertex_up(graph, vertex)
    elif command == "path":
        from_vertex, to_vertex = query_data[1], query_data[2]
        shortest_path, total_time = dijkstra(graph, from_vertex, to_vertex)
        print(' '.join(shortest_path), total_time)
    
    elif command == "print":
        print_graph(graph)
    
    elif command == "reachable":
        reachable = reachable_vertices(graph)
        up_vertices = [node for node in graph.nodes() if 'down' not in graph.nodes[node]]
        up_vertices.sort()
        for node in up_vertices:
            if node in reachable:
                print(node)
                for neighbor in reachable[node]:
                    print(neighbor)

    elif command == "quit":
        sys.exit()
    
    else:
        print("Invalid command")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py network.txt")
        sys.exit(1)
    
    file_name = sys.argv[1]
    graph = build_graph(file_name)
    print("Graph built successfully.")
    
    # Handling queries from standard input
    while True:
        try:
            query = input("Enter query: ")
            if query.lower() == "exit":
                break
            process_query(graph, query)
        except EOFError:
            break
