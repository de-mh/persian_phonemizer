# persian_phonemizer
A tool for translating Persian text to IPA (International Phonetic Alphabet).

In persian, one written word can have different pronunciations and different meanings according to the pronunciation. 
This library helps with disambiguation of such words.

A few examples of use cases of this library are:
* Input for TTS systems
* Helping people in learning Persian
* Adding pronunciation for persian words in texts of other languages

## Usage

Fast start:

```
>>> from persian_phonemizer import Phonemizer
>>> phonemizer = Phonemizer()
>>> phonemizer.phonemize("آن مرد مرد.")
'ʔɒːn mæɾd moɾd .'
>>> phonemizer.phonemize("دوچرخه جدید علی گم شد.")
'dovtʃʰæɾxeje dʒædiːde ʔæliː ɡom ʃod .'
```

If you want to add new data or create the database from scratch, look in the dataset directory.

To-Do list:
- [X] parse Dehkhoda
- [X] parse Moen
- [X] use part-of-speech tagger to identify suiting paronounce
- [X] use dependecy parser to add 'e' between words when needed
- [X] train a model to predict pronounce for words missing from DB
- [X] add lemmatizer for better coverage
- [ ] use Bert to choose from pronounces with same POS
