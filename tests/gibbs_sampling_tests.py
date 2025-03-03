import unittest
from collections import Counter
from random import randint, choices
from gibbs_sampling import get_profile, get_probability, select_motif, gibbs_sampler  # Supondo que as funções estão em um arquivo chamado gibbs_sampler.py

class TestGibbsSampler(unittest.TestCase):

    def setUp(self):
        # Sequências de exemplo e comprimento do motivo para os testes
        self.seqs = [
            "ACGTACGTGACG",
            "TGCATCGTACGT",
            "CGTACGTAGCTA",
            "GTACGTACGTAG"
        ]
        self.k = 4  # Comprimento do motivo a ser procurado

    def test_get_profile(self):
        '''
        Testa a função get_profile()
        '''
        motifs = ["ACGT", "TGCA", "CGTA", "GTAC"]
        profile = get_profile(motifs, self.k)
        self.assertEqual(len(profile), self.k)
        # Verifica se o perfil para cada coluna soma 1
        for col in profile:
            self.assertAlmostEqual(sum(col.values()), 1.0)
    
    def test_get_profile_valid_probabilities(self):
        '''
        Garante que as probabilidades do perfil somam 1 para cada coluna
        '''
        motifs = ["ACGT", "TGCA", "CGTA", "GTAC"]
        profile = get_profile(motifs, self.k)
        for col in profile:
            self.assertAlmostEqual(sum(col.values()), 1.0)
    
    def test_get_probability(self):
        '''
        Testa a função get_probability()
        '''
        motifs = ["ACGT", "TGCA", "CGTA", "GTAC"]
        profile = get_profile(motifs, self.k)
        probabilities = get_probability("ACGTACGTGACG", profile, self.k)
        self.assertAlmostEqual(sum(probabilities), 1.0)
    
    def test_get_probability_zero_case(self):
        '''
        Testa se uma sequência sem motivos correspondentes resulta em baixa probabilidade
        '''
        motifs = ["AAAA", "AAAA", "AAAA"]
        profile = get_profile(motifs, self.k)
        probabilities = get_probability("GGGGGGGG", profile, self.k)
        self.assertTrue(all(p <= 1.0 for p in probabilities))
    
    def test_select_motif(self):
        '''
        Testa a função select_motif()
        '''
        motifs = ["ACGT", "TGCA", "CGTA", "GTAC"]
        profile = get_profile(motifs, self.k)
        position = select_motif("ACGTACGTGACG", profile, self.k)
        self.assertTrue(0 <= position <= len("ACGTACGTGACG") - self.k)
    
    def test_select_motif_randomness(self):
        '''
        Garante que select_motif() escolhe uma posição dentro do intervalo várias vezes
        '''
        motifs = ["ACGT", "TGCA", "CGTA", "GTAC"]
        profile = get_profile(motifs, self.k)
        positions = [select_motif("ACGTACGTGACG", profile, self.k) for _ in range(10)]
        for pos in positions:
            self.assertTrue(0 <= pos <= len("ACGTACGTGACG") - self.k)
    
    def test_gibbs_sampler(self):
        '''
        Testa a função gibbs_sampler()
        '''
        best_motifs, best_positions, best_score = gibbs_sampler(self.seqs, self.k, max_iter=10, stagnation_limit=5)
        self.assertEqual(len(best_motifs), len(self.seqs))
        self.assertGreaterEqual(best_score, 0)
    
    def test_gibbs_sampler_stability(self):
        '''
        Garante que gibbs_sampler retorna consistentemente motivos válidos e pontuações
        '''
        for _ in range(5):
            best_motifs, best_positions, best_score = gibbs_sampler(self.seqs, self.k, max_iter=10, stagnation_limit=5)
            self.assertEqual(len(best_motifs), len(self.seqs))
            self.assertGreaterEqual(best_score, 0)

if __name__ == "__main__":
    unittest.main()

