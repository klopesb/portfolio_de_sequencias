import string

class Automaton:
    """
    A deterministic finite automaton (DFA) designed to search for a given pattern in a sequence.
    Attributes:
        alphabet (list): The list of valid input symbols.
        pattern (str): The target pattern to match in sequences.
        num_states (int): The total number of states in the DFA (pattern length + 1).
        transition_table (list): The transition table mapping states to next states based on input symbols.
    """

    def __init__(self, alphabet, pattern):
        """
        Initializes the Automaton with the given alphabet and pattern.
        Args:
            alphabet (iterable): The set of valid input characters.
            pattern (str): The pattern to search for in sequences.
        """
        self.alphabet = list(alphabet)
        self.pattern = pattern
        self.num_states = len(pattern) + 1
        self.transition_table = self.build_transition_table()

    def build_transition_table(self):
        """
        Builds the transition table for the DFA based on the given pattern.
        Returns:
            list: A list of dictionaries representing state transitions.
        """        
        table = [{ch: 0 for ch in self.alphabet} for _ in range(self.num_states)]

        #Define state transitions based on pattern matching
        for state in range(len(self.pattern)):
            expected_char = self.pattern[state]
            for ch in self.alphabet:
                if ch == expected_char:
                    #Move to the next state if the character matches the expected one
                    table[state][ch] = state + 1
                else:
                    #reset on mismatch
                    table[state][ch] = 0

        #Final state transitions back to 0 - no looping
        for ch in self.alphabet:
            table[self.num_states - 1][ch] = 0
            
        return table

    def apply_to_sequence(self, sequence):
        """
        Processes the sequence and records the states visited by the automaton.
        Args:
            sequence (str): The input sequence to analyze.
        Returns:
            list: A list of visited states during sequence processing.
        """
        state = 0
        visited = []

        for symbol in sequence:
            state = self.transition_table[state].get(symbol, 0)
            visited.append(state)

            #Reset state after full match completion to allow for overlapping matches
            #Reset to 0 after reaching the final state - because its naive
            if state == self.num_states - 1:
                state = 0

        return visited

    def find_pattern_positions(self, sequence):
        """
        Identifies all positions where the pattern appears in the sequence.
        Args:
            sequence (str): The input sequence to search.
        Returns:
            list: A list of starting indices where the pattern is found.
        """
        positions = []
        state = 0

        for i, symbol in enumerate(sequence):
            state = self.transition_table[state].get(symbol, 0)
            if state == len(self.pattern):
                #Final state reached, record the position
                positions.append(i - len(self.pattern) + 1)
                #Reset state to allow for overlapping matches
                state = 0

        return positions

def main():
    """
    Runs the automaton using user input for pattern and sequence analysis.
    Prints the transition table, visited states, and pattern match positions.
    """
    alphabet = string.ascii_lowercase
    pattern = input("Enter the pattern you want to search for: ").strip().lower()
    sequence = input("Enter the sequence where you want to search for the pattern: ").strip().lower()

    automaton = Automaton(alphabet, pattern)

    print("\nTransition Table:")
    for i, row in enumerate(automaton.transition_table):
        print(f"State {i}: {row}")

    print("\nVisited states:", automaton.apply_to_sequence(sequence))
    print("Pattern positions:", automaton.find_pattern_positions(sequence))

if __name__ == "__main__":
    main()