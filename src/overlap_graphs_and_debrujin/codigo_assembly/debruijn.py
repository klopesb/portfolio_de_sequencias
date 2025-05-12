# -*- coding: utf-8 -*-

from MyGraph import MyGraph

class DeBruijnGraph(MyGraph):
    """
    DeBruijnGraph represents a De Bruijn graph for sequence assembly.
    Inherits from MyGraph and provides methods for graph construction,
    edge addition, in-degree calculation, and sequence reconstruction from paths.
    """
    
    def __init__(self, frags):
        """
        Initializes the De Bruijn graph from a list of k-mer fragments.
        """
        MyGraph.__init__(self, {})
        self.create_deBruijn_graph(frags)

    def add_edge(self, o, d):
        """
        Adds a directed edge from vertex o to vertex d, allowing multiple edges between the same pair of nodes.
        Vertices are added if they do not already exist.
        """
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        self.graph[o].append(d)

    def in_degree(self, v):
        """
        Calculates the in-degree of vertex v, accounting for multiple edges.
        """
        res = 0
        for k in self.graph.keys(): 
            if v in self.graph[k]: 
                res += self.graph[k].count(v)
        return res

    def create_deBruijn_graph(self, frags):
        """
        Constructs the De Bruijn graph from a list of k-mer fragments.
        Each fragment creates an edge from its prefix to its suffix.
        """
        for seq in frags:
            suf = suffix(seq)
            self.add_vertex(suf)
            pref = prefix(seq)
            self.add_vertex(pref)
            self.add_edge(pref, suf)
        

    def seq_from_path(self, path):
        """
        Reconstructs the sequence from a given Eulerian path in the De Bruijn graph.
        """
        seq = path[0]
        for i in range(1,len(path)):
            nxt = path[i]
            seq += nxt[-1]
        return seq 
    
def suffix (seq): 
    """
    Returns the suffix of a sequence (all characters except the first).
    """
    return seq[1:]
    
def prefix(seq):
    """
    Returns the prefix of a sequence (all characters except the last).
    """
    return seq[:-1]

def composition(k, seq): 
    """
    Generates all k-length substrings (k-mers) from the input sequence, sorted alphabetically.
    """
    res = []
    for i in range(len(seq)-k+1):
        res.append(seq[i:i+k])
    res.sort()
    return res



def test1():
    """
    Test the creation of a De Bruijn graph using a predefined set of fragments.
    Prints the resulting graph structure.
    """
    frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    dbgr = DeBruijnGraph(frags)
    # Print the structure of the De Bruijn graph
    print("De Bruijn graph:")
    print("Vertex -> Edges")
    dbgr.print_graph()

test1()
print()    
    
def test2():
    """
    Test the Eulerian path functionality of the De Bruijn graph.
    Prints the graph structure, checks for nearly balanced graph, and finds an Eulerian path.
    """
    frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    dbgr = DeBruijnGraph(frags)
    print("De Bruijn graph:")
    dbgr.print_graph()
    print ("nearly balanced graph:", dbgr.check_nearly_balanced_graph())
    print ("Eulerian path:",dbgr.eulerian_path())

test2()
print()

def test3():
    """
    Demonstrates sequence reconstruction from a De Bruijn graph using a given original sequence.
    Prints the graph, checks if it is nearly balanced, finds an Eulerian path, and reconstructs the sequence from the path.
    """
    orig_sequence = "ATGCAATGGTCTGATG"
    frags = composition(3, orig_sequence)
    dbgr = DeBruijnGraph(frags)
    print("Reconstructing sequence from De Bruijn graph:")
    dbgr.print_graph()
    print ("nearly balanced graph:", dbgr.check_nearly_balanced_graph())
    p = dbgr.eulerian_path()
    print ("Eulerian path:", p)
    print ("Original sequence:",dbgr.seq_from_path(p))


test3()
print()

