import spacy
import hazm
import pickle
from g2p_fa import G2P_Fa
from .utils import (
    valid_word,
     Database,
     POS_MODEL_PATH,
     CFG_PATH
)
from .dicts import (
    pos_to_fa,
    IPA_additives,
    eraab_additives
)

class Phonemizer():
    """A class for generating IPA from raw persian text."""

    def __init__(self, output_format="IPA"):
        """Construct normalizer, lemmatizer and G2P, setup settings, load POSTagger, Dependecy Parser and DataBase"""
        if not (output_format in ["IPA", "eraab"]):
            print("outpt_format should be either 'IPA' or 'eraab'")
            raise
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
        """Phonemize text
        Args:
            text: raw persian text

        Returns:
            Phonemized text
        """
        text = self.normalizer.normalize(text)
        phonemized_list = []
        doc = self.nlp (text)
        for idx, _ in enumerate(doc):
            pronounce = self.phonemize_word(doc, idx)
            phonemized_list.append(pronounce)
            self.post_process(doc, idx, phonemized_list)
        return " ".join(phonemized_list)
        
            
    def phonemize_word(self, sentence_tokens, idx):
        """Phonemize a word in a sentence.
        Args:
            sentence_tokens: list of word tokens in a sentence parsed by spacy
            idx: index of target word in the sentence_tokens
        Returns:
            string of phonemized text
        """
        word = sentence_tokens[idx].text
        if not valid_word(word):
            return word

        root = self.lemmatizer.lemmatize(word)
        word_additives = []
        if root != word:
            if '#' in root:
                root_forms = root.split('#')
                for i in range(1):
                    if root_forms[i] != '' and root_forms[i] in word:
                        word_additives = word.split(root_forms[i])
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
            pronounce = self.choose_pronounce(sentence_tokens, idx, pronounces)

        pronounce = self.phonemize_additives(pronounce, word_additives)
        return pronounce

    def phonemize_additives(self, pronounce, word_additives):
        """Add pronunciation for additives of compound words.
        Args:
            pronunce: string of pronunce for base form of word
            word_additives: list of prefix and sffix of word if available
        
        Returns:
            full word pronounce string
        """
        if len(word_additives) == 0:
            return pronounce
        if word_additives[0] != '':
            pronounce = self.additive_dict[word_additives[0].strip('‌')] + pronounce
        if word_additives[1] != '':
            pronounce += self.additive_dict[word_additives[1].strip('‌')]
        return pronounce

    def get_pronounce(self, pronounce):
        """Exteract the pronunciation from pronunciation tuple based on output_format."""
        if self.output_format == "IPA":
            return pronounce[4]
        elif self.output_format == "eraab":
            return pronounce[2]

    def predict_pronounce(self, word):
        """Predict pronunciation of the word using G2P model."""
        if self.output_format == "IPA":
            return self.g2p(word)
        else:
            return word

    def choose_pronounce(self, sentence_tokens, idx, pronounces):
        """Choose the best pronunciation from available ones.
        Args:
            sentence_tokens: list of word tokens in a sentence parsed by spacy
            idx: index of target word in the sentence_tokens
            prononces: list of available pronounces
        Returns:
            string of chosen pronounce
            """
        pos = sentence_tokens[idx].tag_
        for pronounce in pronounces:
            if pronounce[3] == None:
                continue
            if self.translate_pos(pronounce[3]) in pos:
                return self.get_pronounce(pronounce)
        return self.get_pronounce(pronounces[0])       

    def translate_pos(self, pos):
        """Convert pos from DB standard to spacy ouutput."""
        return pos_to_fa.get(pos, "")

    def post_process(self, doc, idx, phonemized_list):
        """Modify pronounce to add e or ye when needed"""
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