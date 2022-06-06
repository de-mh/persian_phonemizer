import unittest
from persian_phonemizer import Phonemizer


class TestPhonemizer(unittest.TestCase):
    def test_Phonemizer_IPA(self):
        phonemizer = Phonemizer()
        cases = [("آرادان", "ʔɒːɾɒːdɒːn"),
         ("این یک متن فارسی است.", "ʔiːn jækʰ mætʰn fɒːɾsiː ʔæstʰ .")]
        for case in cases:
            self.assertEqual(phonemizer.phonemize(case[0]), case[1])

    def test_Phonemizer_eraab(self):
        phonemizer = Phonemizer(output_format="eraab")
        cases = [("آرادان", "آرادان"), ("سلام", "سَلام"), 
         ("این متن فارسی است.", "این مَتن فارسی اَست .")]
        for case in cases:
            self.assertEqual(phonemizer.phonemize(case[0]), case[1])