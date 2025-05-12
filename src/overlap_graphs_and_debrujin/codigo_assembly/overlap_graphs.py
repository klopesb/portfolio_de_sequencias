# -*- coding: utf-8 -*-

from MyGraph import MyGraph

class OverlapGraph(MyGraph):
    """
    OverlapGraph represents an overlap graph for sequence assembly.
    Inherits from MyGraph and provides methods for graph construction,
    handling repeated fragments, and sequence reconstruction from paths.
    """
    
    def __init__(self, frags, reps = True):
        """
        Initializes the OverlapGraph from a list of k-mer fragments.
        If reps is True, handles repeated fragments as unique nodes.
        """
        MyGraph.__init__(self, {})
        if reps:
            self.create_overlap_graph_with_reps (frags)
        else: self.create_overlap_graph(frags)
        self.reps = reps
    
    ## create overlap graph from list of sequences (fragments)
    def create_overlap_graph(self, frags):
        """
        Constructs the overlap graph from a list of fragments.
        Adds vertices and edges where the suffix of one fragment matches the prefix of another.
        """
        for seq in frags:
            self.add_vertex(seq)
        
        #add edges
        for seq in frags:
            suf = suffix(seq)
            for seq2 in frags:
                if prefix(seq2) == suf:
                    self.add_edge(seq, seq2)
        
        
    def create_overlap_graph_with_reps(self, frags):
        """
        Constructs the overlap graph for fragments with possible repetitions.
        Each repeated fragment is treated as a unique node with an identifier.
        """
        idnum = 1
        for seq in frags:
            self.add_vertex(seq+ "-" + str(idnum))
            idnum = idnum + 1
        idnum = 1
        for seq in frags:
            suf = suffix(seq)
            for seq2 in frags:
                if prefix(seq2) == suf:
                    for x in self.get_instances(seq2):
                        self.add_edge(seq+ "-" + str(idnum), x)
            idnum = idnum + 1
    
    def get_instances(self, seq):
        """
        Returns a list of all node names in the graph that contain the given sequence.
        Used to handle repeated fragments.
        """
        res = []
        for k in self.graph.keys():
            if seq in k: res.append(k)
        return res
    
    def get_seq(self, node):
        """
        Returns the sequence associated with a node in the graph.
        If reps is True, removes the unique identifier from the node name.
        """
        if node not in self.graph.keys(): 
            return None
        if self.reps: 
            return node.split("-")[0]
        else: 
            return node
    
    def seq_from_path(self, path):
        """
        Reconstructs the sequence from a given path in the overlap graph.
        Returns None if the path is not Hamiltonian.
        """
        if not self.check_if_hamiltonian_path(path): 
            return None
        seq = self.get_seq(path[0])
        for i in range(1, len(path)):
            nxt = self.get_seq(path[i])
            seq += nxt[-1]
        return seq
                    
# auxiliary
def composition(k, seq):
    """
    Generates all k-length substrings (k-mers) from the input sequence.
    """
    res = []
    for i in range(len(seq)-k+1):
        res.append(seq[i:i+k])
    return res
    
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

  
# testing / mains
def test1():
    seq = "CAATCATGATG"
    k = 3
    print ("Composition in k-mers:",composition(k, seq))

test1()
print()

def test2():
    print("Overlap graph:")
    frags = ["ACC", "ATA", "CAT", "CCA", "TAA"]
    ovgr = OverlapGraph(frags)
    # Expected output: A representation of the overlap graph showing vertices and edges
    ovgr.print_graph()

test2()
print()

def test3():
    print("Create overlap graph from list of sequences (fragments):")
    frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)
    print("Overlap graph: vertex -> edges")
    ovgr.print_graph()

test3()
print()

def test4():
    print("Check if path is hamiltonian:")
    frags = ["ATA",  "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA" , "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags)

    path = ['ACC-2', 'CCA-8', 'CAT-5', 'ATG-3']
    print("Testing path:", path, "- Expected: Valid path and not Hamiltonian")
    print("Valid path:",ovgr.check_if_valid_path(path))
    print("Hamiltonian path:", ovgr.check_if_hamiltonian_path(path))

    path2 = ['ACC-2', 'CCA-8', 'CAT-5', 'ATG-3', 'TGG-13', 'GGC-10', 'GCA-9', 'CAT-6', 'ATT-4', 'TTT-15', 'TTC-14', 'TCA-12', 'CAT-7', 'ATA-1', 'TAA-11']
    print("Testing path:", path2, "- Expected: Valid path and Hamiltonian")
    print("Valid path:",ovgr.check_if_valid_path(path2))
    print("Hamiltonian path:", ovgr.check_if_hamiltonian_path(path2))
    #print (ovgr.seq_from_path(path2))

test4()
print()

def test5():
    frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags)

    path = ovgr.search_hamiltonian_path()
    if path is None:
        print("No Hamiltonian path exists.")
    else:
        print("Hamiltonian path:",path)
        print("Is there a hamiltonian path?",ovgr.check_if_hamiltonian_path(path))
        print("Sequence from Hamiltonian path:",ovgr.seq_from_path(path))

test5()
print()

def test6():
    orig_sequence = "CAATCATGATG"
    frags = composition(3, orig_sequence)
    print ("k-mers:",frags)
    ovgr = OverlapGraph(frags)
    print("Adjacency list -> overlap graph with unique identifier:")
    ovgr.print_graph()
    print("Hamiltonian path with unique identifiers:")
    path = ovgr.search_hamiltonian_path()
    print (path) 
    print ("Original sequence:",ovgr.seq_from_path(path))

test6()

