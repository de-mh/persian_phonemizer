# persian_phonemizer
A tool for translating Persian text to IPA (International Phonetic Alphabet).

In Persian, one written word can have different pronunciations and different meanings according to the pronunciation. 
This library helps with disambiguation of such words.

A few examples of use cases of this library are:
* Input for TTS systems
* Helping people in learning Persian
* Adding pronunciation for Persian words in texts of other languages

## Installation

```
pip install persian_phonemizer
```

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

you can set the package to output Persian text with eraab instead of IPA:

```
>>> phonemizer = Phonemizer(output_format='eraab')
>>> phonemizer.phonemize("آن مرد مرد.")
'آن مَرد مُرد .'
```
## What's inside?

- A database containing words, part-of-speech, pronunciation and meaning according to Moen dictionary
    - script for parsing Dehkhoda dictionary is available in the dataset directory. Still, the results are not used in the package because some pronunciations are outdated and will do more harm than good.
- A Part-of-Speech tagger and a Dependency Parser trained on [Universal Dependencies](https://universaldependencies.org/) dataset using [spaCy](https://spacy.io/)
- A Grapheme to Phoneme model using a seq-to-seq neural network implemented in Pytorch. More info is provided in [g2p_fa](https://github.com/de-mh/g2p_fa) repo.
These assets were created to be used in this repo but each one has the ability to be used separately.

## How does it work?

This package uses several approaches for finding the proper pronunciation. 
1. Input text gets normalized and tokenized
2. Root word for each word in input is calculated using a lemmatizer to cover complex verbs and nouns
3. Each word is looked up for pronunciations in the database.
    - If there is no pronunciation available, pronounce is predicted using [g2p_fa](https://github.com/de-mh/g2p_fa).
    - If there is one pronunciation, that one is used.
    - If there is more than one pronunciation, the correct one is chosen based on the Part-of-Speech tag for that word.
4. Suffix and prefix pronunciations are added for each word
5. Add `e` or `je` between words when needed using the dependency parser
