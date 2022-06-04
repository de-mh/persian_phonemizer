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

```>>> from persian_phonemizer import Phonemizer
>>> phonemizer = Phonemizer()
>>> phonemizer.phonemize("این یک متن فارسی است.")
'ʔiːn jækʰ mætʰn fɒːɾsiː ʔæstʰ .'
```

If you want to add new data or create the database from scratch, look in the dataset directory.
