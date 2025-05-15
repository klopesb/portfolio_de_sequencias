
from Graph import MyGraph
import heapq

class MyWeightedGraph(MyGraph):
    def __init__(self, g={}):
        """
        Constructor for MyWeightedGraph, inherits from MyGraph.
        Initializes the graph with weighted edges (destination_node, weight).
        Ensures all nodes mentioned in edges are added to the graph.
        """
        self.graph = {}
        all_nodes = set()

        if isinstance(g, dict):
            for node, edges in g.items():
                all_nodes.add(node)
                if isinstance(edges, list):
                    for edge in edges:
                        if isinstance(edge, tuple) and len(edge) == 2:
                            destination, weight = edge
                            all_nodes.add(destination) 
                        else:
                            print(f"Warning: Invalid edge format for node {node}: {edge}. Skipping.")
                else:
                    print(f"Warning: Invalid edge list format for node {node}: {edges}. Skipping.")
        else:
            print("Warning: Invalid graph initialization data. Expected a dictionary.")

        for node in all_nodes:
             self.graph[node] = [] 

        if isinstance(g, dict):
             for node, edges in g.items():
                 if isinstance(edges, list):
                     for edge in edges:
                        if isinstance(edge, tuple) and len(edge) == 2:
                             destination, weight = edge
                             if node in self.graph and destination in self.graph:
                                 self.graph[node].append((destination, weight))


    def add_edge(self, o, d, w):
        """
        Adds a weighted edge from node 'o' to node 'd' with weight 'w'.
        If nodes 'o' or 'd' do not exist, they are added.
        Prevents adding a duplicate edge between 'o' and 'd' if one already exists.
        """
        self.add_vertex(o)
        self.add_vertex(d)

        edge_exists = any(neighbor_tuple[0] == d for neighbor_tuple in self.graph.get(o, []))

        if not edge_exists:
             self.graph[o].append((d, w))
        else:
            print(f"Warning: Edge from {o} to {d} already exists. Skipping addition.")

    def get_edges(self):
        """
        Returns the list of edges in the weighted graph as (origin, destination, weight).
        """
        edges = []
        for v in self.graph.keys():
            for d, w in self.graph.get(v, []): 
                edges.append((v, d, w))
        return edges

    
    def get_successors(self, v):
        """
        Returns the list of successor nodes for a given node 'v' (without weights).
        Returns an empty list if the node does not exist.
        """
        return [neighbor_tuple[0] for neighbor_tuple in self.graph.get(v, [])]


    def get_predecessors(self, v):
        """
        Returns the list of predecessor nodes for a given node 'v' (without weights).
        Returns an empty list if the node does not exist or has no predecessors.
        """
        res = []
        for k in self.graph.keys():
            for d, w in self.graph.get(k, []):
                if d == v: 
                    res.append(k)
        return res

    def out_degree(self, v):
        """
        Calculates the out-degree of a node 'v' (number of outgoing edges).
        Returns 0 if the node does not exist.
        """
        return len(self.graph.get(v, []))


    def in_degree(self, v):
        """
        Calculates the in-degree of a node 'v' (number of incoming edges).
        Returns 0 if the node does not exist.
        """
        return len(self.get_predecessors(v))

    def degree(self, v):
        """
        Calculates the degree of a node 'v' (total number of adjacent nodes).
        Returns 0 if the node does not exist.
        """
        return len(self.get_adjacents(v))


    def distance(self, s, d):
        """
        Calculates the shortest distance (sum of weights) between nodes 's' and 'd'
        using Dijkstra's algorithm with a priority queue.
        Returns float('inf') if 'd' is not reachable from 's'.
        Returns None if the start or destination node does not exist.
        """
        if s not in self.graph or d not in self.graph:
            return None
        if s == d:
            return 0

        distances = {node: float('inf') for node in self.graph}
        distances[s] = 0

        priority_queue = [(0, s)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_node == d:
                return current_distance
            if current_distance > distances[current_node]:
                continue
            for neighbor, weight in self.graph.get(current_node, []):
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        return float('inf')


    def shortest_path(self, s, d):
        """
        Finds the shortest path (list of nodes) between nodes 's' and 'd'
        in a weighted graph using Dijkstra's algorithm with a priority queue (heapq).
        Returns None if 'd' is not reachable from 's' or if start/end node doesn't exist.
        """
        if s not in self.graph or d not in self.graph:
            return None
        if s == d:
            return [s]

        distances = {node: float('inf') for node in self.graph}
        distances[s] = 0
        predecessors = {node: None for node in self.graph}

        priority_queue = [(0, s)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_node == d:
                break
            if current_distance > distances[current_node]:
                continue
            for neighbor, weight in self.graph.get(current_node, []):
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        path = []
        current = d
        while current is not None:
            path.insert(0, current)
            current = predecessors[current]
        if path and path[0] != s:
             return None
        if not path and s != d:
            return None
        return path


#Test Functions for MyWeightedGraph

def test_weighted_graph_creation_and_basic_ops():
    print("Testing MyWeightedGraph Creation and Basic Operations")

    g1 = MyWeightedGraph()
    print("Empty weighted graph nodes:", g1.get_nodes())
    print("Empty weighted graph edges:", g1.get_edges())
    print("Empty weighted graph print:")
    g1.print_graph()

    initial_weighted_graph_data = {
        "A": [("B", 10), ("C", 3)],
        "B": [("C", 1), ("D", 2)],
        "C": [("B", 4), ("D", 8), ("E", 2)],
        "D": [("E", 7)],
        "E": [("D", 9), ("F", 1)] 
    }
    g2 = MyWeightedGraph(initial_weighted_graph_data)
    print("Weighted graph g2 nodes:", g2.get_nodes())
    print("Weighted graph g2 edges:", g2.get_edges()) 
    print("Weighted graph g2 print:")
    g2.print_graph() 

def test_weighted_add_vertex_and_edge():
    print("--- Testing add_vertex and add_edge in MyWeightedGraph ---")
    g = MyWeightedGraph()

    g.add_vertex("X")
    g.add_vertex("Y")
    g.add_edge("X", "Y", 5)
    g.add_edge("Y", "Z", 10) 
    g.add_edge("X", "Y", 7) #Test adding duplicate edge 

    print("Graph after additions:")
    g.print_graph() 
    print("Nodes:", g.get_nodes()) 
    print("Edges:", g.get_edges()) 

def test_weighted_degree_calculations():
    print("Testing Degree Calculations in MyWeightedGraph")
    initial_weighted_graph_data = {
        "A": [("B", 10), ("C", 3)],
        "B": [("C", 1), ("D", 2)],
        "C": [("B", 4), ("D", 8), ("E", 2)],
        "D": [("E", 7)],
        "E": [("D", 9), ("F", 1)],
        "F": [] 
    }
    g = MyWeightedGraph(initial_weighted_graph_data)

    print("Graph:")
    g.print_graph()

    print("Out-degree A:", g.out_degree("A"))
    print("In-degree A:", g.in_degree("A"))  
    print("Degree A:", g.degree("A"))  

    print("Out-degree B:", g.out_degree("B")) 
    print("In-degree B:", g.in_degree("B"))
    print("Degree B:", g.degree("B")) 

    print("Out-degree E:", g.out_degree("E")) 
    print("In-degree E:", g.in_degree("E"))
    print("Degree E:", g.degree("E"))

    print("Out-degree F:", g.out_degree("F")) 
    print("In-degree F:", g.in_degree("F"))
    print("Degree F:", g.degree("F"))


    print("Out-degree Z:", g.out_degree("Z")) 
    print("In-degree Z:", g.in_degree("Z"))
    print("Degree Z:", g.degree("Z"))

def test_weighted_shortest_path_and_distance():
    print("Testing Weighted Shortest Path and Distance (Dijkstra)")
    
    initial_weighted_graph_data = {
        "A": [("B", 10), ("C", 3)],
        "B": [("C", 1), ("D", 2)],
        "C": [("B", 4), ("D", 8), ("E", 2)],
        "D": [("E", 7)],
        "E": [("D", 9), ("F", 1)],
        "F": []
    }
    g = MyWeightedGraph(initial_weighted_graph_data)

    print("Graph:")
    g.print_graph()

    print("Distance A to A:", g.distance("A", "A"))
    print("Path A to A:", g.shortest_path("A", "A")) 
   
    print("Distance A to C:", g.distance("A", "C"))
    print("Path A to C:", g.shortest_path("A", "C")) 
   
    print("Distance A to E:", g.distance("A", "E"))
    print("Path A to E:", g.shortest_path("A", "E")) 

    print("Distance A to D:", g.distance("A", "D")) 
    print("Path A to D:", g.shortest_path("A", "D")) 

    print("Distance A to F:", g.distance("A", "F"))
    print("Path A to F:", g.shortest_path("A", "F")) 

    print("Distance F to A:", g.distance("F", "A")) #Expected: inf
    print("Path F to A:", g.shortest_path("F", "A")) #Expected: None

    #Test non-existent nodes
    print("Distance A to Z:", g.distance("A", "Z")) 
    print("Path A to Z:", g.shortest_path("A", "Z"))
    print("Distance Z to A:", g.distance("Z", "A"))
    print("Path Z to A:", g.shortest_path("Z", "A"))


#Run Tests
if __name__ == "__main__":
    test_weighted_graph_creation_and_basic_ops()
    test_weighted_add_vertex_and_edge()
    test_weighted_degree_calculations()
    test_weighted_shortest_path_and_distance()