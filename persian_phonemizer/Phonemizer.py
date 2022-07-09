from distutils.log import error
import spacy
import pickle
from g2p_fa import G2P_Fa
from persian_phonemizer.utils import (
    valid_word,
     Database,
     POS_MODEL_PATH,
     CFG_PATH
)
from persian_phonemizer.dicts import pos_to_fa

class Phonemizer():

    def __init__(self, preserve_punctuations=True, output_format="IPA"):
        if not (output_format in ["IPA", "eraab"]):
            raise error #fix
        self.output_format = output_format
        config = pickle.load(open(CFG_PATH, "rb"))
        lang_cls = spacy.util.get_lang_class(config["nlp"]["lang"])
        self.nlp = lang_cls.from_config(config)
        self.nlp.from_bytes(pickle.load(open(POS_MODEL_PATH, "rb")))
        self.db = Database()
        self.g2p = G2P_Fa()
        
    def phonemize(self, text):
        phonemized_list = []
        doc = self.nlp (text)
        for idx, _ in enumerate(doc):
            pronounce = self.phonemize_word(doc, idx)
            phonemized_list.append(pronounce)
            self.post_process(doc, idx, phonemized_list)
        return " ".join(phonemized_list)
        
            
    def phonemize_word(self, sentence_tokens, idx):
        word = sentence_tokens[idx].text
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
        return self.g2p(word)

    def choose_pronounce(self, sentence_tokens, idx, pronounces):
        pos = sentence_tokens[idx].tag_
        # print(sentence_tokens)
        for pronounce in pronounces:
            if pronounce[3] == None:
                continue
            if self.translate_pos(pronounce[3]) in pos:
                return self.get_pronounce(pronounce)
        # warning : no match
        return self.get_pronounce(pronounces[0])       

    def translate_pos(self, pos):
        return pos_to_fa.get(pos, "")

    def post_process(self, doc, idx, phonemized_list):
        vowels = 'æeoː' if self.output_format == 'IPA' else 'ایو'
        if phonemized_list[idx][-2:] == 'eh':
            phonemized_list[idx] = phonemized_list[idx][:-1]
        if doc[idx].dep_ in ['nmod', 'amod']:
            if phonemized_list[-2][-1] in vowels:
                phonemized_list[-2] += 'je' if self.output_format == 'IPA' else '‌ی'
            else:
                phonemized_list[-2] += 'e' if self.output_format == 'IPA' else 'ِ'

    def __del__(self):
        del self.db