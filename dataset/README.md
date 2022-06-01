## Creating Database

`process.py` is a script for creating a sql database containing word with eraab, POS, IPA and meaning for each word in Dehkhoda dictionary.

The package contains the dataset and you don't need to do these steps for using the project. This script is mainly included as an example of how to add new data.

To run the script, first downloaded Dehkhoda dataset from `https://github.com/DehkhodaProject/DehkhodaProject/releases` and extract it in this directory then,

delete zero files with `find . -type f -size 0 -delete`

and finally run `process.py`