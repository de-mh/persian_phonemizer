from distutils.log import error
import hazm
from persian_phonemizer.utils import (
    valid_word,
     Database,
     POS_MODEL_PATH
)

class Phonemizer():

    def __init__(self, normalize=True, preserve_punctuations=True, output_format="IPA"):
        if not (output_format in ["IPA", "eraab"]):
            raise error #fix
        self.output_format = output_format
        self.normalize = normalize
        self.tagger = hazm.POSTagger(model=POS_MODEL_PATH)
        if normalize:
            self.normalizer = hazm.Normalizer()
        self.db = Database()
        
    def phonemize(self, text):
        if self.normalize:
            text = self.normalizer.normalize(text)
        phonemized_list = []
        for sentence in hazm.sent_tokenize(text):
            sentence_tokens = hazm.word_tokenize(sentence)
            for idx, _ in enumerate(sentence_tokens):
                pronounce = self.phonemize_word(sentence_tokens, idx)
                phonemized_list.append(pronounce)
        return " ".join(phonemized_list)
        
            
    def phonemize_word(self, sentence_tokens, idx):
        word = sentence_tokens[idx]
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
            pronounce = self.choose_pronounce(self, sentence_tokens, idx, pronounces)
        return pronounce

    def get_pronounce(self, pronounce):
        if self.output_format == "IPA":
            return pronounce[4]
        elif self.output_format == "eraab":
            return pronounce[2]

    def predict_pronounce(self, word):
        return word

    def choose_pronounce(self, sentence_tokens, idx, pronounces):
        tagged_list = self.tagger.tag(sentence_tokens)
        word, pos = tagged_list[idx]
        persian_pos = translate_pos(pos)
        for pronounce in pronounces:
            if persian_pos in pronounce[3]:
                return self.get_pronounce(pronounce)
        # warning : no match
        return self.get_pronounce(pronounces[0])       



    def __del__(self):
        del self.db