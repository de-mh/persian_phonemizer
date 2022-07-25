import unittest
from persian_phonemizer import Phonemizer


class TestPhonemizer(unittest.TestCase):
    def test_Phonemizer_IPA(self):
        phonemizer = Phonemizer()
        cases = [
            ("نمی‌رفتیم", "nemiːɾæftʰiːm"),
            ("کتاب علی را بردند.", "kʰetʰɒːbe ʔæliː ɾɒː boɾdænd ."),
            ("آن مرد مرد.", "ʔɒːn mæɾd moɾd ."),
            ("دوچرخه جدید علی گم شد.", "dovtʃʰæɾxeje dʒædiːde ʔæliː ɡom ʃod .")
            ]
        for case in cases:
            self.assertEqual(phonemizer.phonemize(case[0]), case[1])

    def test_Phonemizer_eraab(self):
        phonemizer = Phonemizer(output_format="eraab")
        cases = [
            ("نمی‌گفتیم", "نِمی\u200cگُفتیم"), ("سلام", "سَلام"), 
            ("کتاب علی را بردند.", "کِتابِ علی را بُردَند ."),
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