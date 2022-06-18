from distutils.log import error
from parsivar import (
    Normalizer,
     Tokenizer,
      POSTagger
)
from persian_phonemizer.utils import (
    valid_word,
     Database
)

class Phonemizer():

    def __init__(self, normalize=True, preserve_punctuations=True, output_format="IPA"):
        if not (output_format in ["IPA", "eraab"]):
            raise error #fix
        self.output_format = output_format
        self.tokenizer = Tokenizer()
        self.normalize = normalize
        self.tagger = POSTagger(tagging_model="wapiti")
        if normalize:
            self.normalizer = Normalizer()
        self.db = Database()
        
    def phonemize(self, text):
        if self.normalize:
            text = self.normalizer.normalize(text)
        phonemized_list = []
        for sentence in self.tokenizer.tokenize_sentences(text):
            sentence_tokens = self.tokenizer.tokenize_words(sentence)
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
            pronounce = self.choose_pronounce(sentence_tokens, idx, pronounces)
        return pronounce

    def get_pronounce(self, pronounce):
        if self.output_format == "IPA":
            return pronounce[4]
        elif self.output_format == "eraab":
            return pronounce[2]

    def predict_pronounce(self, word):
        return word

    def choose_pronounce(self, sentence_tokens, idx, pronounces):
        tagged_list = self.tagger.parse(sentence_tokens)
        word, pos = tagged_list[idx]
        persian_pos = self.translate_pos(pos)
        for pronounce in pronounces:
            if pronounce[3] == None:
                continue
            if persian_pos in pronounce[3]:
                return self.get_pronounce(pronounce)
        # warning : no match
        return self.get_pronounce(pronounces[0])       

    def translate_pos(self, pos):
        return pos

    def __del__(self):
        del self.db