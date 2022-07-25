import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as requirements_file:
        requirements = requirements_file.read().splitlines()

setuptools.setup(
    name="persian_phonemizer",
    version="0.4.0",
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
    install_requires=requirements,
    package_data={'persian_phonemizer': ['data/*']},
    python_requires=">=3.6",
)