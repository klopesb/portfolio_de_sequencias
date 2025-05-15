class MyGraph:

    def __init__(self, g = {}):
        '''
        Constructor for a directed graph using an adjacency list with lists.
        Takes a dictionary where keys are nodes and values are iterables of successor nodes.
        Default is an empty dictionary.
        Note: Uses lists for adjacency, which means checking for neighbor existence is O(k).
        '''
        self.graph = {k: list(v) for k, v in g.items()}

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v])

    ## get basic info

    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())

    def get_edges(self):
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph.get(v, []):
                edges.append((v,d))
        return edges

    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())

    ## add nodes and edges

    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph:
            self.graph[v] = []

    def add_edge(self, o, d):
        '''
        Add a directed edge to the graph from origin 'o' to destination 'd'.
        If vertices do not exist, they are added to the graph.
        Adds the edge only if it doesn't already exist.
        '''
        if o not in self.graph: self.add_vertex(o)
        if d not in self.graph: self.add_vertex(d)
        if d not in self.graph[o]:
             self.graph[o].append(d)


    ## successors, predecessors, adjacent nodes

    def get_successors(self, v):
        '''
        Returns a list of successor nodes of vertex v.
        Returns an empty list if the vertex does not exist or has no successors.
        Returns a copy to prevent external modification of the internal list.
        '''
        return list(self.graph.get(v, []))

    def get_predecessors(self, v):
        '''
        Returns a list of predecessor nodes of vertex v.
        Returns an empty list if the vertex does not exist or has no predecessors.
        Note: This is an O(V*k) operation in the worst case (V nodes, max k neighbors).
        '''
        res = []
        for k in self.graph.keys():
            if v in self.graph.get(k, []):
                res.append(k)
        return res

    def get_adjacents(self, v):
        '''
        Returns a list of adjacent nodes (successors and predecessors) of vertex v.
        Considers the graph edges bidirectionally for the purpose of adjacency.
        Returns an empty list if the vertex does not exist or has no adjacent nodes.
        '''
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        adjacents = list(pred)
        for p in suc:
             if p not in adjacents:
                 adjacents.append(p)
        return adjacents

    ## degrees

    def out_degree(self, v):
        ''' Returns the out-degree of vertex v. Returns 0 if the vertex does not exist. '''
        return len(self.graph.get(v, []))

    def in_degree(self, v):
        '''
        Returns the in-degree of vertex v.
        Returns 0 if the vertex does not exist or has no predecessors.
        Note: This involves scanning all adjacency lists.
        '''
        count = 0
        for k in self.graph.keys():
            if v in self.graph.get(k, []):
                count += 1
        return count


    def degree(self, v):
        '''
        Returns the total degree of vertex v (number of unique adjacent nodes).
        Returns 0 if the vertex does not exist or has no adjacent nodes.
        '''
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        return len(set(suc).union(set(pred)))


    def _get_all_out_degrees(self):
        ''' Computes the out-degree for all nodes. Returns {node: out_degree}. '''
        return {v: len(self.graph.get(v, [])) for v in self.graph.keys()}

    def _get_all_in_degrees(self):
        ''' Computes the in-degree for all nodes. Returns {node: in_degree}. '''
        in_degs = {v: 0 for v in self.graph.keys()}
        for v in self.graph.keys():
            for d in self.graph.get(v, []):
                if d in in_degs:
                     in_degs[d] += 1
        return in_degs

    def all_degrees(self, deg_type = "inout"):
        '''
        Computes the degree (of a given type) for all nodes.
        deg_type can be "in", "out", or "inout" (default).
        Returns a dictionary {node: degree}.
        '''
        if deg_type == "out":
            return self._get_all_out_degrees()
        elif deg_type == "in":
            return self._get_all_in_degrees()
        elif deg_type == "inout":
            return {v: self.degree(v) for v in self.graph.keys()}
        else:
             print(f"Warning: Invalid deg_type '{deg_type}'. Use 'in', 'out', or 'inout'.")
             return {}


    def highest_degrees(self, all_deg= None, deg_type = "inout", top= 10):
        '''
        Returns a list of nodes with the highest degrees.
        Takes a dictionary of degrees (all_deg) or computes it using all_degrees.
        deg_type can be "in", "out", or "inout".
        By default, returns the top 10 nodes by total degree.
        '''
        if all_deg is None:
            all_deg = self.all_degrees(deg_type)
        ord_deg = sorted(list(all_deg.items()), key=lambda x : x[1], reverse = True)
        return ord_deg[:top]


    ## topological metrics over degrees

    def mean_degree(self, deg_type = "inout"):
        '''
        Computes the mean degree (of a given type) for all nodes.
        deg_type can be "in", "out", or "inout".
        Returns 0.0 for an empty graph.
        '''
        degs = self.all_degrees(deg_type)
        if not degs: return 0.0
        return sum(degs.values()) / float(len(degs))

    def prob_degree(self, deg_type = "inout"):
        '''
        Computes the probability distribution of degrees (of a given type).
        deg_type can be "in", "out", or "inout".
        Returns a dictionary where keys are degrees and values are their probabilities.
        Returns an empty dictionary for an empty graph.
        '''
        degs = self.all_degrees(deg_type)
        if not degs: return {}
        res = {}
        for k in degs.keys():
            degree_val = degs[k]
            if degree_val in res:
                res[degree_val] += 1
            else:
                res[degree_val] = 1
        num_nodes = float(len(degs))
        for k in res:
            res[k] /= num_nodes
        return res


    ## BFS and DFS searches

    def reachable_bfs(self, v):
        '''
        Performs a Breadth-First Search (BFS) starting from vertex v
        and returns a list of all reachable nodes (excluding v itself).
        Returns an empty list if the vertex does not exist or no nodes are reachable.
        '''
        if v not in self.graph: return []
        q = [v]
        res = []
        visited = {v}

        while q:
            node = q.pop(0)

            for elem in self.graph.get(node, []):
                if elem not in visited:
                    q.append(elem)
                    visited.add(elem)
                    if elem != v: res.append(elem)
        return res

    def reachable_dfs(self, v):
        '''
        Performs a Depth-First Search (DFS) starting from vertex v
        and returns a list of all reachable nodes (excluding v itself).
        The order of nodes in the result depends on the traversal order.
        Returns an empty list if the vertex does not exist or no nodes are reachable.
        Note: Uses an iterative approach with a stack.
        '''
        if v not in self.graph: return []
        stack = [v]
        res = []
        visited = {v}

        while stack:
            node = stack.pop()

            if node != v:
                res.append(node)

            neighbors = list(self.graph.get(node, []))
            neighbors.reverse()

            for neighbor in neighbors:
                 if neighbor not in visited:
                     visited.add(neighbor)
                     stack.append(neighbor)

        return res


    def distance(self, s, d):
        '''
        Calculates the shortest path distance from source s to destination d
        in an unweighted graph using BFS.
        Returns the distance (number of edges) or None if d is unreachable from s
         or if s or d do not exist.
        Returns 0 if s == d.
        '''
        if s == d: return 0
        if s not in self.graph or d not in self.graph: return None

        q = [(s,0)]
        visited = {s}

        while q:
            node, dist = q.pop(0)

            for elem in self.graph.get(node, []):
                if elem == d: return dist + 1
                if elem not in visited:
                    q.append((elem,dist+1))
                    visited.add(elem)
        return None


    def shortest_path(self, s, d):
        '''
        Finds one shortest path from source s to destination d
        in an unweighted graph using BFS.
        Returns a list of nodes representing the path, or None if d is unreachable from s
        or if s or d do not exist.
        Returns [s] if s == d.
        '''
        if s == d: return [s]
        if s not in self.graph or d not in self.graph: return None

        q = [(s,[])]
        visited = {s}

        while q:
            node, path_to_node = q.pop(0)

            for elem in self.graph.get(node, []):
                if elem == d: return path_to_node + [node, elem]
                if elem not in visited:
                    q.append((elem, path_to_node + [node]))
                    visited.add(elem)
        return None


    def reachable_with_dist(self, s):
        '''
        Performs a BFS starting from vertex s and returns a list of tuples
        (node, distance) for all reachable nodes (excluding s itself).
        Returns an empty list if the vertex does not exist or no other nodes are reachable.
        '''
        if s not in self.graph: return []

        res = []
        q = [(s,0)]
        visited = {s}

        while q:
            node, dist = q.pop(0)

            if node != s:
                 res.append((node,dist))

            for elem in self.graph.get(node, []):
                 if elem not in visited:
                    q.append((elem,dist+1))
                    visited.add(elem)
        return res

    ## mean distances ignoring unreachable nodes
    def mean_distances(self):
        '''
        Computes the mean distance between all reachable pairs of nodes (s, d) where s != d.
        Also returns the proportion of reachable pairs out of all possible distinct pairs n*(n-1).
        Returns (0.0, 0.0) for graphs with 0 or 1 node or if no pairs are reachable.
        '''
        tot = 0
        num_reachable = 0

        nodes = self.get_nodes()
        n = len(nodes)

        if n <= 1:
            return 0.0, 0.0

        for k in self.graph.keys():
            distsk = self.reachable_with_dist(k)

            for _, dist in distsk:
                 tot += dist
            num_reachable += len(distsk)

        if num_reachable == 0:
            meandist = 0.0
        else:
             meandist = float(tot) / num_reachable

        total_possible_pairs = n * (n - 1)
        if total_possible_pairs == 0:
             proportion_reachable = 0.0
        else:
            proportion_reachable = float(num_reachable) / total_possible_pairs

        return meandist, proportion_reachable


    def closeness_centrality(self, node):
        '''
        Computes the closeness centrality of a node.
        Calculated as (number of reachable nodes from node) / (sum of distances to those reachable nodes).
        Returns 0.0 if no other nodes are reachable from the node or if the node doesn't exist.
        Note: This is the version for potentially disconnected graphs, considering only reachable nodes.
        '''
        dist = self.reachable_with_dist(node)

        if len(dist) == 0:
             return 0.0

        s = 0.0
        for d in dist:
             s += d[1] 
        return float(len(dist)) / s


    def highest_closeness(self, top = 10):
        '''
        Returns a list of nodes with the highest closeness centrality.
        By default, returns the top 10 nodes.
        '''
        cc = {}
        for k in self.graph.keys():
            cc[k] = self.closeness_centrality(k)
        ord_cl = sorted(list(cc.items()), key=lambda x : x[1], reverse = True)
        return [x[0] for x in ord_cl[:top]]


    def betweenness_centrality(self, node):
        '''
        (Naive Implementation)
        Computes a measure related to betweenness centrality by counting,
        for each pair of distinct nodes (s, t) different from 'node',
        if 'node' lies on *one* shortest path found between s and t using BFS.
        Returns the count of such paths divided by the total number of shortest paths found (which is at most 1 per pair (s,t) in this implementation).
        Note: This implementation does NOT count all shortest paths between s and t,
        and thus does NOT compute the standard betweenness centrality for graphs
        with multiple shortest paths. It's an approximation based on finding one path.
        Returns 0.0 if the graph has fewer than 3 nodes or no paths are found between valid pairs.
        '''
        nodes = self.get_nodes()
        if len(nodes) < 3 or node not in nodes:
            return 0.0

        total_sp_count = 0
        sps_with_node_count = 0

        for s in nodes:
            for t in nodes:
                if s != t and s != node and t != node:
                    path = self.shortest_path(s, t)
                    if path is not None:
                        total_sp_count += 1
                        if node in path[1:-1]:
                             sps_with_node_count += 1

        if total_sp_count == 0:
            return 0.0

        return float(sps_with_node_count) / total_sp_count


    ## cycles

    def node_has_cycle (self, v):
        '''
        Checks if a directed cycle exists starting from and returning to vertex v.
        Uses a BFS-based approach (checking reachability back to the start node).
        Returns True if a cycle through v is detected, False otherwise or if v doesn't exist.
        Note: Uses lists for queue and visited tracking, potentially impacting performance on large graphs.
        '''
        if v not in self.graph:
            return False

        q = [v]
        visited = [v]

        while len(q) > 0:
            node = q.pop(0)

            for neighbor in self.graph.get(node, []):
                if neighbor == v:
                    return True
                elif neighbor not in visited:
                    q.append(neighbor)
                    visited.append(neighbor)

        return False


    def has_cycle(self):
        '''
        Checks if the graph contains any directed cycle.
        Checks if any node in the graph can reach itself via a directed path (indicating a cycle).
        Returns True if any directed cycle is found, False otherwise.
        Note: This implementation has O(V * (V+E)) time complexity in the worst case.
        '''
        for node in self.graph.keys():
            if self.node_has_cycle(node):
                return True
        return False


    ## clustering

    def clustering_coef(self, v):
        '''
        Computes the local clustering coefficient for a directed graph at vertex v.
        Calculated as (number of directed edges between neighbors of v) / (k * (k-1)),
        where k is the number of adjacent nodes (successors + predecessors), k > 1.
        Returns 0.0 if v has 1 or fewer adjacent nodes or if v doesn't exist.
        Note: 'Adjacent' includes both incoming and outgoing neighbors,
        and the formula counts directed edges between them.
        '''
        if v not in self.graph: return 0.0

        adjs = self.get_adjacents(v)
        k = len(adjs)
        if k <= 1: return 0.0

        ligs = 0
        for i in adjs:
             for j in adjs:
                 if i != j:
                     if i in self.graph and j in self.graph.get(i, []):
                          ligs += 1

        denominator = k * (k - 1)

        if denominator == 0:
            return 0.0
        return float(ligs) / denominator


    def all_clustering_coefs(self):
        ''' Computes the clustering coefficient for all nodes in the graph. '''
        ccs = {}
        for k in self.graph.keys():
            ccs[k] = self.clustering_coef(k)
        return ccs

    def mean_clustering_coef(self):
        ''' Computes the average clustering coefficient across all nodes. '''
        ccs = self.all_clustering_coefs()
        if not ccs: return 0.0
        return sum(ccs.values()) / float(len(ccs))

    def mean_clustering_perdegree(self, deg_type = "inout"):
        '''
        Computes the average clustering coefficient for nodes grouped by their degree.
        deg_type can be "in", "out", or "inout" (default).
        Returns a dictionary where keys are degrees and values are the average clustering coefficient for nodes with that degree.
        Returns an empty dictionary for an empty graph.
        '''
        degs = self.all_degrees(deg_type)
        ccs = self.all_clustering_coefs()
        degs_k = {}

        for node, degree_value in degs.items():
            if degree_value not in degs_k:
                degs_k[degree_value] = []
            degs_k[degree_value].append(node)

        ck = {}
        for degree_value, nodes_with_degree in degs_k.items():
            total_cc_for_degree = 0
            for v in nodes_with_degree:
                 total_cc_for_degree += ccs.get(v, 0.0)
            ck[degree_value] = float(total_cc_for_degree) / len(nodes_with_degree)
        return ck


# Test Functions for MyGraph

def test_basic_info():
    print("Basic Tests")
    g_empty = MyGraph()
    print("\nTesting Empty Graph:")
    g_empty.print_graph()
    print("Nodes:", g_empty.get_nodes())
    print("Edges:", g_empty.get_edges())
    print("Size (nodes, edges):", g_empty.size())

    g_simple = MyGraph({'A':['B','C'], 'B':['C'], 'C':['B','D'], 'D':['B']})
    print("\nTesting Simple Graph (g_simple):")
    g_simple.print_graph()
    print("Nodes:", g_simple.get_nodes())
    print("Edges:", g_simple.get_edges())
    print("Size (nodes, edges):", g_simple.size())
    print("-" * 20)

def test_add_elements():
    print("Tests for Adding Elements")
    g = MyGraph()
    print("\nAdding vertices and edges:")
    g.add_vertex('A')
    print("Graph after adding A:", g.graph)
    g.add_vertex('B')
    print("Graph after adding B:", g.graph)
    g.add_edge('A', 'B')
    print("Graph after adding A->B:", g.graph)
    g.add_edge('B', 'C')
    print("Graph after adding B->C:", g.graph)
    g.add_edge('B', 'A')
    print("Graph after adding B->A:", g.graph)
    g.add_edge('C', 'D')
    print("Graph after adding C->D:", g.graph)
    g.add_vertex('A')
    print("Graph after trying to add A again:", g.graph)
    g.add_edge('X', 'Y')
    print("Graph after adding X->Y (new nodes):", g.graph)
    print("\nFinal Graph:")
    g.print_graph()
    print("Nodes:", g.get_nodes())
    print("Edges:", g.get_edges())
    print("Size (nodes, edges):", g.size())
    print("-" * 20)

def test_neighbors():
    print("Tests for Neighbors")
    g = MyGraph({'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['D'], 'D': []})
    print("Testing on graph:")
    g.print_graph()
    print("\nSuccessors of A:", g.get_successors('A'))
    print("Successors of B:", g.get_successors('B'))
    print("Successors of C:", g.get_successors('C'))
    print("Successors of D:", g.get_successors('D'))
    print("Successors of Z:", g.get_successors('Z'))
    print("\nPredecessors of A:", g.get_predecessors('A'))
    print("Predecessors of B:", g.get_predecessors('B'))
    print("Predecessors of D:", g.get_predecessors('D'))
    print("Predecessors of Z:", g.get_predecessors('Z'))
    print("\nAdjacents of A:", g.get_adjacents('A'))
    print("Adjacents of B:", g.get_adjacents('B'))
    print("Adjacents of D:", g.get_adjacents('D'))
    print("Adjacents of Z:", g.get_adjacents('Z'))
    print("-" * 20)

def test_degrees():
    print("Tests for Degrees")
    g = MyGraph({'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['D'], 'D': []})
    print("Testing on graph:")
    g.print_graph()
    print("\nOut-degree of A:", g.out_degree('A'))
    print("In-degree of A:", g.in_degree('A'))
    print("Total degree of A:", g.degree('A'))
    print("\nOut-degree of D:", g.out_degree('D'))
    print("In-degree of D:", g.in_degree('D'))
    print("Total degree of D:", g.degree('D'))
    print("\nDegrees of all nodes (out):", g.all_degrees("out"))
    print("Degrees of all nodes (in):", g.all_degrees("in"))
    print("Degrees of all nodes (total):", g.all_degrees())
    all_deg_total = g.all_degrees("inout")
    print("Nodes with highest degree (total, top 2):", g.highest_degrees(all_deg=all_deg_total, deg_type="inout", top=2))
    print("Mean degree (total):", g.mean_degree())
    print("Degree probability distribution (total):", g.prob_degree())
    g_empty = MyGraph()
    print("\nTesting degrees on empty graph:")
    print("Degrees of all nodes (total):", g_empty.all_degrees())
    print("Mean degree (total):", g_empty.mean_degree())
    print("Degree probability distribution (total):", g_empty.prob_degree())
    print("-" * 20)

def test_traversal_distance():
    print("Tests for Traversal and Distance")
    g = MyGraph({'A':['B','C'], 'B':['D','E'], 'C':['E'], 'D':[], 'E':['F'], 'F':[]})
    print("Testing on graph:")
    g.print_graph()
    print("\nReachable from A (BFS):", g.reachable_bfs('A'))
    print("Reachable from A (DFS):", g.reachable_dfs('A'))
    print("Reachable from D (BFS):", g.reachable_bfs('D'))
    print("Reachable from F (BFS):", g.reachable_bfs('F'))
    print("\nDistance from A to F:", g.distance('A', 'F'))
    print("Distance from A to D:", g.distance('A', 'D'))
    print("Distance from A to A:", g.distance('A', 'A'))
    print("Distance from F to A:", g.distance('F', 'A'))
    print("Distance from A to Z:", g.distance('A', 'Z'))
    print("\nShortest path from A to F:", g.shortest_path('A', 'F'))
    print("Shortest path from A to D:", g.shortest_path('A', 'D'))
    print("Shortest path from F to A:", g.shortest_path('F', 'A'))
    print("Shortest path from A to A:", g.shortest_path('A', 'A'))
    print("\nReachable with distance from A:", g.reachable_with_dist('A'))
    print("Reachable with distance from D:", g.reachable_with_dist('D'))
    print("\nMean distances and proportion reachable (g):", g.mean_distances())
    g_disconnected = MyGraph({'A': ['B'], 'B': ['A'], 'C': ['D'], 'D': ['C']})
    print("\nTesting on disconnected graph:")
    g_disconnected.print_graph()
    print("Mean distances and proportion reachable (g_disconnected):", g_disconnected.mean_distances())
    g_one_node = MyGraph({'A': []})
    print("\nTesting on graph with 1 node:")
    g_one_node.print_graph()
    print("Mean distances and proportion reachable (g_one_node):", g_one_node.mean_distances())
    print("-" * 20)

def test_centrality():
    print("Tests for Centrality")
    g_closeness = MyGraph({'A':['B','C'], 'B':['D','E'], 'C':['E'], 'D':['F'], 'E':['F'], 'F':[]})
    print("Testing closeness centrality on graph:")
    g_closeness.print_graph()
    print("\nCloseness centrality of A:", g_closeness.closeness_centrality('A'))
    print("Closeness centrality of E:", g_closeness.closeness_centrality('E'))
    print("Closeness centrality of F:", g_closeness.closeness_centrality('F'))
    print("Closeness centrality of Z:", g_closeness.closeness_centrality('Z'))
    print("Nodes with highest closeness centrality (top 3):", g_closeness.highest_closeness(top=3))
    g_betweenness = MyGraph({'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': ['E']})
    print("\nTesting betweenness centrality on graph:")
    g_betweenness.print_graph()
    print("Betweenness centrality of D:", g_betweenness.betweenness_centrality('D'))
    print("Betweenness centrality of B:", g_betweenness.betweenness_centrality('B'))
    print("Betweenness centrality of A:", g_betweenness.betweenness_centrality('A'))
    print("Betweenness centrality of E:", g_betweenness.betweenness_centrality('E'))
    g_cycle_betweenness = MyGraph({'A': ['B'], 'B': ['C'], 'C': ['A', 'D'], 'D': ['E']})
    print("\nTesting betweenness centrality on graph with a cycle:")
    g_cycle_betweenness.print_graph()
    print("Betweenness centrality of C:", g_cycle_betweenness.betweenness_centrality('C'))
    g_small = MyGraph({'A': ['B']})
    print("\nTesting betweenness centrality on small graph (2 nodes):")
    g_small.print_graph()
    print("Betweenness centrality of A:", g_small.betweenness_centrality('A'))
    print("-" * 20)

def test_cycles():
    print("Tests for Cycles")
    g_cycle1 = MyGraph({'A':['B'], 'B':['C'], 'C':['A']})
    print("\nTesting on graph g_cycle1:")
    g_cycle1.print_graph()
    print("Graph has cycle starting from A?", g_cycle1.node_has_cycle('A'))
    print("Graph has cycle starting from B?", g_cycle1.node_has_cycle('B'))
    print("Graph has cycle overall?", g_cycle1.has_cycle())
    g_cycle2 = MyGraph({'A':['B'], 'B':['C', 'D'], 'C':['A']})
    print("\nTesting on graph g_cycle2:")
    g_cycle2.print_graph()
    print("Graph has cycle starting from A?", g_cycle2.node_has_cycle('A'))
    print("Graph has cycle starting from D?", g_cycle2.node_has_cycle('D'))
    print("Graph has cycle overall?", g_cycle2.has_cycle())
    g_no_cycle = MyGraph({'A':['B','C'], 'B':['D','E'], 'C':['E'], 'D':[], 'E':['F'], 'F':[]})
    print("\nTesting on acyclic graph g_no_cycle:")
    g_no_cycle.print_graph()
    print("Graph has cycle starting from A?", g_no_cycle.node_has_cycle('A'))
    print("Graph has cycle starting from F?", g_no_cycle.node_has_cycle('F'))
    print("Graph has cycle overall?", g_no_cycle.has_cycle())
    g_self_loop = MyGraph({'A':['A']})
    print("\nTesting on graph with self-loop g_self_loop:")
    g_self_loop.print_graph()
    print("Graph has cycle starting from A?", g_self_loop.node_has_cycle('A'))
    print("Graph has cycle overall?", g_self_loop.has_cycle())
    g_disconnected_cycle = MyGraph({'A':['B'], 'B':['A'], 'C':['D'], 'D':['C']})
    print("\nTesting on graph with disconnected cycles:")
    g_disconnected_cycle.print_graph()
    print("Graph has cycle starting from A?", g_disconnected_cycle.node_has_cycle('A'))
    print("Graph has cycle starting from C?", g_disconnected_cycle.node_has_cycle('C'))
    print("Graph has cycle overall?", g_disconnected_cycle.has_cycle())
    print("-" * 20)

def test_clustering():
    print("Tests for Clustering")
    g_clustering = MyGraph({'A': ['B', 'C', 'D'], 'B': ['A', 'C'], 'C': ['A', 'B', 'D'], 'D': ['A', 'C']})
    print("\nTesting on graph g_clustering:")
    g_clustering.print_graph()
    print("\nAdjacents of A:", g_clustering.get_adjacents('A'))
    print("Clustering coefficient of A:", g_clustering.clustering_coef('A'))
    print("Adjacents of B:", g_clustering.get_adjacents('B'))
    print("Clustering coefficient of B:", g_clustering.clustering_coef('B'))
    print("Adjacents of D:", g_clustering.get_adjacents('D'))
    print("Clustering coefficient of D:", g_clustering.clustering_coef('D'))
    print("\nAll clustering coefficients:", g_clustering.all_clustering_coefs())
    print("Mean clustering coefficient:", g_clustering.mean_clustering_coef())
    g_deg_cluster_alpha = MyGraph({'A':['B','C'], 'B':['A','C'], 'C':['A','B','D'], 'D':['C','E'], 'E':['D']})
    print("\nTesting Clustering per Degree (g_deg_cluster_alpha):")
    g_deg_cluster_alpha.print_graph()
    print("Degrees (inout):", g_deg_cluster_alpha.all_degrees("inout"))
    print("Clustering coefficients:", g_deg_cluster_alpha.all_clustering_coefs())
    print("Clustering per degree (inout):", g_deg_cluster_alpha.mean_clustering_perdegree("inout"))
    print("-" * 20)


#Run Tests
if __name__ == "__main__":
    test_basic_info()
    test_add_elements()
    test_neighbors()
    test_degrees()
    test_traversal_distance()
    test_centrality()
    test_cycles()
    test_clustering()