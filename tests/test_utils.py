import unittest
from persian_phonemizer.utils import valid_word

class TestValidWord(unittest.TestCase):
    def test_valid_word(self):
        cases = ["شیر", "سلامت", "سَرد", "سیری", "نیازئ", "ءتَغییر", "سویَش"]
        for case in cases:
            self.assertTrue(valid_word(case))
    def test_invalid_pronounces(self):
        cases = ["در ", ",لُ", "،اش", "شَ،سبر", "؟نوبلس"]
        for case in cases:
            self.assertFalse(valid_word(case))
