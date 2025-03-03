import unittest
from branch_and_bound import branch_and_bound

class TestBranchAndBound(unittest.TestCase):
    
    def test_branch_and_bound(self):
        """
        Test the branch_and_bound function with a typical case where there are multiple DNA sequences.
        Verifies that the returned best positions and score are of the correct types (list, integer and 
        non-negative) and that the score is non-negative.
        """
        seqs = ["ACGTG", "ACGTT", "ACGTC"]
        num_seqs = 3
        motif_size = 3
        best_pos, best_score = branch_and_bound(seqs, num_seqs, motif_size)

        self.assertIsInstance(best_pos, list)
        self.assertIsInstance(best_score, int)
        self.assertGreaterEqual(best_score, 0)

    def test_branch_and_bound_single_sequence(self):
        """
        Test the branch_and_bound function with a single DNA sequence.
        Ensures that the function can handle a single sequence and returns valid positions and score.
        """
        seqs = ["ACGTG"]
        num_seqs = 1
        motif_size = 3
        best_pos, best_score = branch_and_bound(seqs, num_seqs, motif_size)

        self.assertIsInstance(best_pos, list)  
        self.assertIsInstance(best_score, int) 
        self.assertGreaterEqual(best_score, 0)

    def test_branch_and_bound_identical_sequences(self):
        """
        Test the branch_and_bound function with identical sequences.
        In this case, the score should be maximized since all columns will have the same character.
        """
        seqs = ["AAAAA", "AAAAA", "AAAAA"]
        num_seqs = 3
        motif_size = 3
        best_pos, best_score = branch_and_bound(seqs, num_seqs, motif_size)

        self.assertEqual(best_score, 9)
        self.assertEqual(best_pos, [0, 0, 0])
        
    def test_empty_sequences(self):
        """
        Test the branch_and_bound function with empty sequences.
        The function should return None for positions and 0 for the score when no sequences are provided.
        """
        seqs = []
        num_seqs = 0
        motif_size = 3
        best_pos, best_score = branch_and_bound(seqs, num_seqs, motif_size)
        self.assertEqual(best_pos, [])
        self.assertEqual(best_score, 0)
    
    def test_empty_sequences_with_motif_size_zero(self):
        """
        Test the branch_and_bound function with motif size zero.
        The function should return an empty list for positions and 0 for the score when the motif size 
        is zero.
        """
        seqs = ["ACGT", "TGCA", "GATT"]
        num_seqs = len(seqs)
        motif_size = 0
        best_pos, best_score = branch_and_bound(seqs, num_seqs, motif_size)
        self.assertEqual(best_pos, [])
        self.assertEqual(best_score, 0)
    
    def test_different_sequence_lengths(self):
        """
        Test the branch_and_bound function with sequences of different lengths.
        The function should raise a ValueError since sequences must be of the same length.
        """
        seqs = ["ACGT", "ACGTTG", "AC"]
        with self.assertRaises(ValueError):
            branch_and_bound(seqs, len(seqs), 3)

    def test_motif_longer_than_sequence(self):
        """
        Test the branch_and_bound function with a motif longer than the sequence length.
        The function should raise a ValueError since the motif cannot be longer than the sequence.
        """
        seqs = ["ACGT", "TGCA", "GATT"]
        num_seqs = len(seqs)
        motif_size = 10
        with self.assertRaises(ValueError):
            branch_and_bound(seqs, num_seqs, motif_size)

    def test_motif_equal_to_sequence_length(self):
        """
        Test the branch_and_bound function with a motif size equal to the sequence length.
        The function should return valid positions and score for this edge case.
        """
        seqs = ["ACGT", "TGCA", "GATT"]
        num_seqs = len(seqs)
        motif_size = 4
        best_pos, best_score = branch_and_bound(seqs, num_seqs, motif_size)
        self.assertEqual(best_score, 5)
        self.assertEqual(best_pos, [0, 0, 0])
        
    def test_protein_sequences(self):
        """
        Test the branch_and_bound function with protein sequences.
        Ensures that the function works with sequences of amino acids and returns a valid score.
        """
        seqs = ["MKVAVL", "MKVAVM", "MKVAVV"]
        num_seqs = len(seqs)
        motif_size = 3
        best_pos, best_score = branch_and_bound(seqs, num_seqs, motif_size)
        self.assertGreaterEqual(best_score, 0)
        self.assertEqual(len(best_pos), num_seqs)
        self.assertTrue(all(pos >= 0 for pos in best_pos))

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
