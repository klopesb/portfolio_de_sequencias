import unittest
import string
from automaton import Automaton  # Ensure automaton.py contains your Automaton class

class TestAutomaton(unittest.TestCase):
    """
    Unit tests for the Automaton class, verifying its functionality in recognizing patterns,
    processing sequences, and handling edge cases.
    """
    def setUp(self):
        """
        Sets up a sample automaton instance before each test.
        Initializes the automaton with an alphabet and a predefined pattern.
        """
        self.alphabet = string.ascii_lowercase
        self.pattern = "abc"
        self.automaton = Automaton(self.alphabet, self.pattern)

    def test_transition_table(self):
        """
        Verifies that the transition table is built correctly.
        Ensures each state transitions according to the expected DFA behavior.
        """
        # Ensure the alphabet is only the relevant characters
        self.alphabet = ['a', 'b', 'c']
        
        # Construct the expected transitions dynamically based on the automaton's behavior
        expected_transitions_abc = [
            {'a': 1, 'b': 0, 'c': 0},  # State 0 transitions
            {'a': 0, 'b': 2, 'c': 0},  # State 1 transitions
            {'a': 0, 'b': 0, 'c': 3},  # State 2 transitions
            {'a': 0, 'b': 0, 'c': 0},  # State 3 transitions (final state)
        ]
        
        # Loop over each state and symbol, and check the actual transitions
        for state in range(self.automaton.num_states):  # num_states is len(pattern) + 1
            for symbol in self.alphabet:
                actual_transition = self.automaton.transition_table[state].get(symbol, 0)
                expected_transition = expected_transitions_abc[state].get(symbol, 0)
                
                # Print out the actual vs. expected transitions for debugging
                print(f"State {state}, Symbol '{symbol}' -> Actual: {actual_transition}, Expected: {expected_transition}")
                
                self.assertEqual(actual_transition, expected_transition)


    def test_apply_to_sequence(self):
        """
        Tests the automaton's sequence processing behavior.
        Verifies that the visited states match expected DFA execution.
        """        
        seq1 = "xyzabc"  # Expected: [0, 0, 0, 1, 2, 3]
        seq2 = "abcdefg"  # Expected: [1, 2, 3, 0, 0, 0, 0]
        seq3 = "xxabcyyabc"  # Expected: [0, 0, 1, 2, 3, 0, 0, 1, 2, 3]
        seq4 = "zzyyz"  # Expected: [0, 0, 0, 0, 0]
        
        self.assertEqual(self.automaton.apply_to_sequence(seq1), [0, 0, 0, 1, 2, 3])
        self.assertEqual(self.automaton.apply_to_sequence(seq2), [1, 2, 3, 0, 0, 0, 0])
        self.assertEqual(self.automaton.apply_to_sequence(seq3), [0, 0, 1, 2, 3, 0, 0, 1, 2, 3])
        self.assertEqual(self.automaton.apply_to_sequence(seq4), [0, 0, 0, 0, 0])  # Non-matching sequence

    def test_find_pattern_positions(self):
        """
        Tests whether the automaton correctly identifies and returns pattern positions in sequences.
        """
        seq1 = "xyzabcxyz"  # Expected: [3]
        seq2 = "abcabcabc"  # Expected: [0, 3, 6]
        seq3 = "defghijkl"  # Expected: []
        seq4 = "aaabbbabcabc"  # Expected: [6, 9]
        
        self.assertEqual(self.automaton.find_pattern_positions(seq1), [3])
        self.assertEqual(self.automaton.find_pattern_positions(seq2), [0, 3, 6])
        self.assertEqual(self.automaton.find_pattern_positions(seq3), [])
        self.assertEqual(self.automaton.find_pattern_positions(seq4), [6,9])  # Overlapping pattern

    def test_edge_cases(self):
        """Tests edge cases including empty inputs, nonexistent patterns, and short sequences."""
        empty_seq = ""
        single_char_seq = "a"
        seq_without_pattern = "xyzxyzxyz"
        empty_pattern = ""  # Empty pattern case
        short_seq = "ab"  # Sequence shorter than pattern
        
        self.assertEqual(self.automaton.apply_to_sequence(empty_seq), [])
        self.assertEqual(self.automaton.apply_to_sequence(single_char_seq), [1])  # Should transition to state 1
        self.assertEqual(self.automaton.find_pattern_positions(seq_without_pattern), [])
        self.assertEqual(self.automaton.find_pattern_positions(empty_pattern), [])  # Empty pattern should have no positions
        self.assertEqual(self.automaton.apply_to_sequence(short_seq), [1, 2])  # Short sequences
        
    def test_overlapping_matches(self):
        """
        Ensures overlapping matches are detected correctly.
        """
        automaton = Automaton(self.alphabet, "abc")
        sequence = "abcabcabcabc"
        expected_positions = [0, 3, 6, 9]
        self.assertEqual(automaton.find_pattern_positions(sequence), expected_positions)

    def test_single_character_pattern(self):
        """
        Verifies automaton behavior for single-character patterns.
        """
        automaton = Automaton(self.alphabet, "a")
        sequence = "aaabc"
        expected_states = [1, 1, 1, 0, 0]
        expected_positions = [0, 1, 2]
        self.assertEqual(automaton.apply_to_sequence(sequence), expected_states)
        self.assertEqual(automaton.find_pattern_positions(sequence), expected_positions)

    def test_non_alphabet_symbols(self):
        """
        Tests automaton behavior with sequences containing non-alphabet symbols.
        """
        sequence = "a!b@c#abc"
        expected_states = [1, 0, 0, 0, 0, 0, 1, 2, 3]
        self.assertEqual(self.automaton.apply_to_sequence(sequence), expected_states)
        self.assertEqual(self.automaton.find_pattern_positions(sequence), [6])

    def test_long_input(self):
        """
        Tests automaton performance with long sequences.
        """
        sequence = "abc" * 1000
        expected_positions = [i * 3 for i in range(1000)]
        self.assertEqual(self.automaton.find_pattern_positions(sequence), expected_positions)

if __name__ == "__main__":
    unittest.main()
