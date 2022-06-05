import unittest
from persian_phonemizer import Phonemizer


class TestPhonemizer(unittest.TestCase):
    def test_Phonemizer(self):
        phonemizer = Phonemizer()
        cases = [("آرادان", "ʔɒːɾɒːdɒːn"),
         ("این یک متن فارسی است.", "ʔiːn jækʰ mætʰn fɒːɾsiː ʔæstʰ .")]
        for case in cases:
            self.assertEqual(phonemizer.phonemize(case[0]), case[1])