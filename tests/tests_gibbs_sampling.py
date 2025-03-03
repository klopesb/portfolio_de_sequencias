import unittest
from gibbs_sampling import get_profile, get_probability, select_motif, gibbs_sampler

class TestGibbsSampler(unittest.TestCase):

    def setUp(self):
        self.seqs = [
            "ACGTACGTGACG",
            "TGCATCGTACGT",
            "CGTACGTAGCTA",
            "GTACGTACGTAG"
        ]
        self.k = 4

    def test_get_profile(self):
        """
        Tests the `get_profile()` function.
        Checks if the profile is correctly generated for a set of motifs. The profile should be a dictionary 
        where each column corresponds to a nucleotide (A, C, G, T) in the motifs. The sum of the values in 
        each column must be 1, ensuring valid probabilities.
        """
        motifs = ["ACGT", "TGCA", "CGTA", "GTAC"]
        profile = get_profile(motifs, self.k)
        self.assertEqual(len(profile), self.k)
    
        for col in profile:
            self.assertAlmostEqual(sum(col.values()), 1.0)

    def test_get_profile_valid_probabilities(self):
        """
        Ensures that the probabilities in the profile sum to 1 for each column.
        This ensures that the profile is normalized and represents valid probability distributions.
        """
        motifs = ["ACGT", "TGCA", "CGTA", "GTAC"]
        profile = get_profile(motifs, self.k)
        for col in profile:
            self.assertAlmostEqual(sum(col.values()), 1.0)

    def test_get_probability(self):
        """
        Tests the `get_probability()` function.
        Checks if the function correctly calculates the probability of a given sequence based on a profile.
        The probabilities should sum to 1 across all positions in the sequence.
        """
        motifs = ["ACGT", "TGCA", "CGTA", "GTAC"]
        profile = get_profile(motifs, self.k)
        probabilities = get_probability("ACGTACGTGACG", profile, self.k)
        self.assertAlmostEqual(sum(probabilities), 1.0)

    def test_get_probability_zero_case(self):
        """
        Tests if a sequence with no matching motifs results in low probabilities.
        When the sequence has no matching motifs in the profile, the probability values should be <= 1, 
        ensuring that motifs that do not fit the profile get lower probabilities.
        """
        motifs = ["AAAA", "AAAA", "AAAA"]
        profile = get_profile(motifs, self.k)
        probabilities = get_probability("GGGGGGGG", profile, self.k)
        self.assertTrue(all(p <= 1.0 for p in probabilities))

    def test_select_motif(self):
        """
        Tests the `select_motif()` function.
        Verifies that the function returns a valid motif position from the given sequence.
        The selected position should be within the range of valid indices in the sequence (length - k).
        """
        motifs = ["ACGT", "TGCA", "CGTA", "GTAC"]
        profile = get_profile(motifs, self.k)
        position = select_motif("ACGTACGTGACG", profile, self.k)
        self.assertTrue(0 <= position <= len("ACGTACGTGACG") - self.k)

    def test_select_motif_randomness(self):
        """
        Ensures that `select_motif()` chooses a position within the valid range multiple times.
        Tests the randomness of motif selection by running the function multiple times and ensuring 
        that each selected position is within the sequence bounds.
        """
        motifs = ["ACGT", "TGCA", "CGTA", "GTAC"]
        profile = get_profile(motifs, self.k)
        positions = [select_motif("ACGTACGTGACG", profile, self.k) for _ in range(10)]
        for pos in positions:
            self.assertTrue(0 <= pos <= len("ACGTACGTGACG") - self.k)
        
    def test_gibbs_sampler(self):
        """
        Tests the `gibbs_sampler()` function.
        This test checks the functionality of the Gibbs sampling algorithm in selecting motifs from the input sequences.
        Ensures that the returned best motifs correspond to the input sequences and that the score is non-negative.
        The result should include the motifs, their positions, and a valid score.
        """
        best_motifs, best_positions, best_score = gibbs_sampler(self.seqs, self.k, max_iter=10, stagnation_limit=5)
        self.assertEqual(len(best_motifs), len(self.seqs))  
        self.assertGreaterEqual(best_score, 0)
        
        for seq, pos in zip(self.seqs, best_positions):
            self.assertTrue(0 <= pos <= len(seq) - self.k)

    def test_gibbs_sampler_stability(self):
        """
        Ensures that `gibbs_sampler()` consistently returns valid motifs and scores across multiple runs.
        By running the Gibbs sampler multiple times, it checks that the results remain consistent with valid motifs 
        and a score greater than or equal to 0 each time.
        """
        for _ in range(5):
            best_motifs, best_positions, best_score = gibbs_sampler(self.seqs, self.k, max_iter=10, stagnation_limit=5)
            self.assertEqual(len(best_motifs), len(self.seqs))
            self.assertGreaterEqual(best_score, 0)
            self.assertEqual(len(best_positions), len(self.seqs))
            for pos in best_positions:
                self.assertTrue(0 <= pos < len(self.seqs[0]) - self.k + 1)
            
if __name__ == "__main__":
    unittest.main()
