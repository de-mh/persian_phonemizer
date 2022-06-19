import unittest
from process_dehkhoda import (
    validate_pronounce,
    extract_IPA
    )

class TestValidatePronounce(unittest.TestCase):
    def test_valid_pronounces(self):
        cases = ["شیر", "آفت", "سَرد", "سیری", "نیاز", "تَغییر", "سویَش"]
        for case in cases:
            self.assertTrue(validate_pronounce(case))
    def test_invalid_pronounces(self):
        cases = ["در", "لُ", "اش", "ش", "َش", "شَسبر", "نوبلس"]
        for case in cases:
            self.assertFalse(validate_pronounce(case))

class TestExtractIPA(unittest.TestCase):
    def test_extract_IPA(self):
        cases = [("آرادان", "ʔɒːɾɒːdɒːn"), ("آتابَیک", "ʔɒːtʰɒːbæjkʰ"), ("بینی", "biːniː"), ("اَبناء", "ʔæbnɒːʔ")]
        for case in cases:
            self.assertEqual(extract_IPA(case[0]), case[1])