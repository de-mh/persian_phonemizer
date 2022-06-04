from distutils.log import error
import hazm
from regex import W
from utils import valid_word, Database

class Phonemizer():

    def __init__(self, normalize=True, preserve_punctuations=True, output_format="IPA"):
        if not (output_format in ["IPA", "eraab"]):
            raise error #fix
        self.output_format = output_format
        self.normalize = normalize
        if normalize:
            self.normalizer = hazm.Normalizer()
        self.db = Database()
        
    def phonemize(self, text):
        if self.normalize:
            text = self.normalizer.normalize(text)
        phonemized_list = []
        for sentence in hazm.sent_tokenize(text):
            for word in hazm.word_tokenize(sentence):
                pronounce = self.phonemize_word(word)
                phonemized_list.append(pronounce)
        return " ".join(phonemized_list)
        
            
    def phonemize_word(self, word):
        if not valid_word(word):
            return word
        pronounces = self.db.lookup_word(word)
        pronounces_count = len(pronounces)
        if pronounces_count == 0:
            pronounce = self.predict_pronounce(word)
        elif pronounces_count == 1:
            pronounce = self.get_pronounce(pronounces[0])
        else:
            # needs disambiguation
            pronounce = self.get_pronounce(pronounces[0])
        return pronounce

    def get_pronounce(self, word):
        if self.output_format == "IPA":
            return word[4]
        elif self.output_format == "eraab":
            return word[2]

    def predict_pronounce(self, word):
        return None



    def __del__(self):
        del self.db