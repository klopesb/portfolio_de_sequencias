import unittest
import random

# Supondo que seu código está em um arquivo chamado motif_finder.py
from gibbs_sampling import (
    inicializar_posicoes_aleatorias,
    construir_pwm,
    calcular_probabilidades_motifs,
    selecionar_motif,
    algoritmo_motif,
    validar_sequencias
)

class TestMotifFinder(unittest.TestCase):

    def setUp(self):
        self.seqs = [
            "GTAAACAATATTTATAGC",
            "AAAATTTACCTCGCAAGG",
            "CCGTACTGTCAAGCGTGG",
            "TGAGTAAACGACGTCCCA",
            "TACTTAACACCCTGTCAA"
        ]
        self.tam_motif = 8
        random.seed(42)

    def test_inicializar_posicoes_aleatorias(self):
        start_pos, limite = inicializar_posicoes_aleatorias(self.seqs, self.tam_motif)
        self.assertEqual(len(start_pos), len(self.seqs))
        self.assertTrue(all(0 <= pos < limite for pos in start_pos))

    def test_construir_pwm_shape_and_prob(self):
        start_pos, _ = inicializar_posicoes_aleatorias(self.seqs, self.tam_motif)
        PWM, motifs = construir_pwm(self.seqs, start_pos, self.tam_motif, excluir_idx=2)
        self.assertEqual(len(PWM), self.tam_motif)
        for pos_probs in PWM:
            total = sum(pos_probs.values())
            self.assertAlmostEqual(total, 1.0, delta=0.05)  # Devido à pseudocontagem

    def test_calcular_probabilidades_motifs(self):
        start_pos, limite = inicializar_posicoes_aleatorias(self.seqs, self.tam_motif)
        PWM, _ = construir_pwm(self.seqs, start_pos, self.tam_motif, excluir_idx=0)
        norm_prob, prob_motif = calcular_probabilidades_motifs(self.seqs[0], PWM, self.tam_motif, limite)
        self.assertAlmostEqual(sum(norm_prob.values()), 1.0, delta=0.01)

    def test_selecionar_motif(self):
        fake_probs = {"AAAAAAAT": 0.1, "TTTTTTTT": 0.3, "CCCCCCCC": 0.6}
        selected = selecionar_motif(fake_probs)
        self.assertIn(selected, fake_probs)

    def test_algoritmo_motif(self):
        best_motifs, best_score = algoritmo_motif(self.seqs, self.tam_motif, max_iter=10, stagnation_limit=5)
        self.assertEqual(len(best_motifs), len(self.seqs))
        self.assertIsInstance(best_score, float)

    def test_validar_sequencias_invalidas(self):
        seqs_invalidas = ["ATGC", "TGXA", "CCCC", "GGGN"]
        with self.assertRaises(ValueError):
            validar_sequencias(seqs_invalidas)

    def test_validar_sequencias_validas(self):
        seqs_validas = ["ATGC", "TGCA", "CCCC", "GGGA"]
        try:
            validar_sequencias(seqs_validas)
        except ValueError:
            self.fail("validar_sequencias() levantou ValueError em sequência válida.")

if __name__ == '__main__':
    unittest.main()
