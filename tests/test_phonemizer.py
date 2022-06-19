import unittest
from persian_phonemizer import Phonemizer


class TestPhonemizer(unittest.TestCase):
    def test_Phonemizer_IPA(self):
        phonemizer = Phonemizer()
        cases = [("فارسی", "fɒːɾsiː"),
         ("این یک متن فارسی است.", "ʔiːn jækʰ mætʰn fɒːɾsiː ʔæstʰ ."),
         ("آن مرد مرد.", "ʔɒːn mæɾd moɾd .")]
        for case in cases:
            self.assertEqual(phonemizer.phonemize(case[0]), case[1])

    def test_Phonemizer_eraab(self):
        phonemizer = Phonemizer(output_format="eraab")
        cases = [("فارسی", "فارسی"), ("سلام", "سَلام"), 
         ("این متن فارسی است.", "این مَتن فارسی اَست ."),
         ("آن مرد مرد.", "آن مَرد مُرد .")]

        for case in cases:
            self.assertEqual(phonemizer.phonemize(case[0]), case[1])