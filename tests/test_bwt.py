import unittest
from bwt import bwt_transform, bwt_reverse_transform

class TestBWT(unittest.TestCase):

    def test_basic_string(self):
        original = "banana"
        expected_bwt = "annb$aa"
        bwt_result, rotations = bwt_transform(original)
        self.assertEqual(bwt_result, expected_bwt)
        decoded = bwt_reverse_transform(bwt_result)
        self.assertEqual(decoded, original + '$')

    def test_empty_string(self):
        original = ""
        expected_bwt = "$"
        bwt_result, rotations = bwt_transform(original)
        self.assertEqual(bwt_result, expected_bwt)
        decoded = bwt_reverse_transform(bwt_result)
        self.assertEqual(decoded, original + '$')

    def test_single_character(self):
        original = "a"
        expected_bwt = "a$"
        bwt_result, rotations = bwt_transform(original)
        self.assertEqual(bwt_result, expected_bwt)
        decoded = bwt_reverse_transform(bwt_result)
        self.assertEqual(decoded, original + '$')

    def test_repeated_characters(self):
        original = "aaaa"
        expected_bwt = "aaaa$"
        bwt_result, rotations = bwt_transform(original)
        self.assertEqual(bwt_result, expected_bwt)
        decoded = bwt_reverse_transform(bwt_result)
        self.assertEqual(decoded, original + '$')

    def test_palindrome(self):
        original = "racecar"
        bwt_result, _ = bwt_transform(original)
        decoded = bwt_reverse_transform(bwt_result)
        self.assertEqual(decoded, original + '$')

    def test_rotations_are_sorted(self):
        original = "banana"
        _, rotations = bwt_transform(original)
        self.assertEqual(rotations, sorted(rotations))

if __name__ == "__main__":
    unittest.main()
