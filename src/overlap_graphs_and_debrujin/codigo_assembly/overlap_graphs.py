from MyGraph import MyGraph

def composition(k, seq):
    """Generates all k-length substrings (k-mers) from the input sequence."""
    return [seq[i:i+k] for i in range(len(seq)-k+1)]

def suffix(seq):
    """Returns the suffix of a sequence (all characters except the first)."""
    return seq[1:]

def prefix(seq):
    """Returns the prefix of a sequence (all characters except the last)."""
    return seq[:-1]

class OverlapGraph(MyGraph):
    """
    OverlapGraph represents an overlap graph for sequence assembly.
    Inherits from MyGraph and provides methods for graph construction,
    handling repeated fragments, and sequence reconstruction from paths.
    """

    def __init__(self, frags, reps=False):
        """
        Initializes the OverlapGraph from a list of k-mer fragments.
        If reps is True, handles repeated fragments as unique nodes.
        """
        super().__init__({})
        self.reps = reps
        if reps:
            self._create_overlap_graph_with_reps(frags)
        else:
            self._create_overlap_graph(frags)

    def _create_overlap_graph(self, frags):
        """Constructs the overlap graph from a list of fragments."""
        for seq in frags:
            self.add_vertex(seq)
        for seq in frags:
            suf = suffix(seq)
            for seq2 in frags:
                if prefix(seq2) == suf:
                    self.add_edge(seq, seq2)

    def _create_overlap_graph_with_reps(self, frags):
        """Constructs the overlap graph for fragments with possible repetitions."""
        nodes = [f"{seq}-{i+1}" for i, seq in enumerate(frags)]
        for node in nodes:
            self.add_vertex(node)
        for i, seq in enumerate(frags):
            suf = suffix(seq)
            src = f"{seq}-{i+1}"
            for j, seq2 in enumerate(frags):
                if prefix(seq2) == suf:
                    for x in self.get_instances(seq2):
                        self.add_edge(src, x)

    def get_instances(self, seq):
        """Returns a list of all node names in the graph that contain the given sequence."""
        return [k for k in self.graph.keys() if seq in k]

    def get_seq(self, node):
        """Returns the sequence associated with a node in the graph."""
        if node not in self.graph:
            return None
        return node.split("-")[0] if self.reps else node

    def seq_from_path(self, path):
        """Reconstructs the sequence from a given path in the overlap graph."""
        if not self.check_if_hamiltonian_path(path):
            return None
        seq = self.get_seq(path[0])
        for node in path[1:]:
            nxt = self.get_seq(node)
            seq += nxt[-1]
        return seq

def custom_test():
    """Allows the user to input a custom sequence and k-mer size, then builds and analyzes the overlap graph."""
    user_seq = input("Enter your sequence: ").upper()
    k = int(input("Enter k-mer size: "))
    if k > len(user_seq):
        print("k-mer size cannot be greater than sequence length.")
        return
    frags = composition(k, user_seq)
    print(f"\nk-mers: {frags}")
    ovgr = OverlapGraph(frags)
    print("\nAdjacency list (overlap graph):")
    ovgr.print_graph()
    path = ovgr.search_hamiltonian_path()
    if path is None:
        print("\nNo Hamiltonian path exists for this set of k-mers.")
    else:
        print("\nHamiltonian path found:", path)
        print("Reconstructed sequence:", ovgr.seq_from_path(path))

def test1():
    """Test for composition in k-mers."""
    seq = "CAATCATGATG"
    k = 3
    print("Composition in k-mers:", composition(k, seq))

def test2():
    """Test for overlap graph construction."""
    print("Overlap graph:")
    frags = ["ACC", "ATA", "CAT", "CCA", "TAA"]
    ovgr = OverlapGraph(frags)
    ovgr.print_graph()

def test3():
    """Test for creating overlap graph from list of sequences (fragments)."""
    print("Create overlap graph with unique identifiers from list of sequences (fragments):")
    frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)
    print("Overlap graph: vertex -> edges")
    ovgr.print_graph()

def test4():
    """Test to check if a path is Hamiltonian."""
    print("Check if path is hamiltonian:")
    frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)
    path = ['ACC-2', 'CCA-8', 'CAT-5', 'ATG-3']
    print("Testing path:", path, "- Expected: Valid path and not Hamiltonian")
    print("Valid path:", ovgr.check_if_valid_path(path))
    print("Hamiltonian path:", ovgr.check_if_hamiltonian_path(path))
    path2 = ['ACC-2', 'CCA-8', 'CAT-5', 'ATG-3', 'TGG-13', 'GGC-10', 'GCA-9', 'CAT-6', 'ATT-4', 'TTT-15', 'TTC-14', 'TCA-12', 'CAT-7', 'ATA-1', 'TAA-11']
    print("Testing path:", path2, "- Expected: Valid path and Hamiltonian")
    print("Valid path:", ovgr.check_if_valid_path(path2))
    print("Hamiltonian path:", ovgr.check_if_hamiltonian_path(path2))

def test5():
    """Test for searching Hamiltonian path in the overlap graph."""
    frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags)
    path = ovgr.search_hamiltonian_path()
    if path is None:
        print("No Hamiltonian path exists.")
    else:
        print("Hamiltonian path:", path)
        print("Is there a hamiltonian path?", ovgr.check_if_hamiltonian_path(path))
        print("Sequence from Hamiltonian path:", ovgr.seq_from_path(path))

def test6():
    """Test for verifying the original sequence and its recovery."""
    orig_sequence = "CAATCATGATG"
    frags = composition(3, orig_sequence)
    print("k-mers:", frags)
    ovgr = OverlapGraph(frags)
    print("Adjacency list -> overlap graph:")
    ovgr.print_graph()
    print("Hamiltonian path:")
    path = ovgr.search_hamiltonian_path()
    print(path)
    print("Original sequence:", ovgr.seq_from_path(path))

def main_menu():
    """Provides a menu for running all predefined tests or a custom test with user input."""
    print("\n=== Overlap Graph Test Menu ===")
    print("1 - Run all predefined tests")
    print("2 - Run custom test with your own sequence and k-mer size")
    choice = input("Choose an option (1 or 2): ")
    if choice == "1":
        print('-------------------------------------------------------------------------')
        print('Tests for Overlap Graphs')
        test1()
        print()
        test2()
        print()
        test3()
        print()
        test4()
        print()
        test5()
        print()
        test6()
        print()
    elif choice == "2":
        custom_test()
    else:
        print("Invalid option. Exiting.")

if __name__ == "__main__":
    main_menu()
