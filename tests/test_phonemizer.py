import unittest
from persian_phonemizer import Phonemizer


class TestPhonemizer(unittest.TestCase):
    def test_Phonemizer_IPA(self):
        phonemizer = Phonemizer()
        cases = [
            ("فارسی", "fɒːɾsiː"),
            ("این یک متن فارسی است.", "ʔiːn jækʰ mætʰne fɒːɾsiː ʔæstʰ ."),
            ("آن مرد مرد.", "ʔɒːn mæɾd moɾd ."),
            ("دوچرخه جدید علی گم شد.", "dovtʃʰæɾxeje dʒædiːde ʔæliː ɡom ʃod .")
            ]
        for case in cases:
            self.assertEqual(phonemizer.phonemize(case[0]), case[1])

    def test_Phonemizer_eraab(self):
        phonemizer = Phonemizer(output_format="eraab")
        cases = [
            ("فارسی", "فارسی"), ("سلام", "سَلام"), 
            ("این متن فارسی است.", "این مَتنِ فارسی اَست ."),
            ("آن مرد مرد.", "آن مَرد مُرد .")
            ]
        for case in cases:
            self.assertEqual(phonemizer.phonemize(case[0]), case[1])

    def test_Phonemizer_predict(self):
        phonemizer = Phonemizer()
        cases = [
            ('سلام', 'sælɒːm')
        ]
        for case in cases:
            self.assertEqual(phonemizer.predict_pronounce(case[0]), case[1])