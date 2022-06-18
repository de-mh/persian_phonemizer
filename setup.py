import setuptools
from pathlib import Path

this_dir = Path(__file__).parent

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="persian_phonemizer",
    version="0.0.1",
    author="Mohamadhosein Dehghani",
    author_email="demh1377@gmail.com",
    description="A tool for translating Persian text to IPA (International Phonetic Alphabet)A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/de-mh/persian_phonemizer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["persian_phonemizer"],
    install_requires=['parsivar'],
    package_data={'persian_phonemizer': ['data/*.db']},
    python_requires=">=3.6",
)