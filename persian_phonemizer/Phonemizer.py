from distutils.log import error
import spacy
import hazm
import pickle
from g2p_fa import G2P_Fa
from persian_phonemizer.utils import (
    valid_word,
     Database,
     POS_MODEL_PATH,
     CFG_PATH
)
from persian_phonemizer.dicts import (
    pos_to_fa,
    IPA_additives,
    eraab_additives
)

class Phonemizer():

    def __init__(self, preserve_punctuations=True, output_format="IPA"):
        if not (output_format in ["IPA", "eraab"]):
            raise error #fix
        self.additive_dict = IPA_additives if output_format == "IPA" else eraab_additives
        self.output_format = output_format
        self.normalizer = hazm.Normalizer()
        self.lemmatizer = hazm.Lemmatizer()
        config = pickle.load(open(CFG_PATH, "rb"))
        lang_cls = spacy.util.get_lang_class(config["nlp"]["lang"])
        self.nlp = lang_cls.from_config(config)
        self.nlp.from_bytes(pickle.load(open(POS_MODEL_PATH, "rb")))
        self.db = Database()
        self.g2p = G2P_Fa()
        
    def phonemize(self, text):
        text = self.normalizer.normalize(text)
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

        root = self.lemmatizer.lemmatize(word)
        word_additives = []
        if root != word:
            if '#' in root:
                root_forms = root.split('#')
                for i in range(1):
                    if root_forms[i] in word:
                        word_additives = word.split(root_forms[0])
                        word = root_forms[i]
            else:
                word_additives = word.split(root)
                word = root

        pronounces = self.db.lookup_word(word)
        pronounces_count = len(pronounces)
        if pronounces_count == 0:
            pronounce = self.predict_pronounce(word)
        elif pronounces_count == 1:
            pronounce = self.get_pronounce(pronounces[0])
        else:
            pronounce = self.choose_pronounce(sentence_tokens, idx, pronounces)4

        pronounce = self.phonemize_additives(pronounce, word_additives)
        return pronounce

    def phonemize_additives(self, pronounce, word_additives):
        if len(word_additives) == 0:
            return pronounce
        pronounce = self.additive_disct[word_additives[0]] + pronounce
        pronounce += self.additive_dict[word_additives[1]]

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