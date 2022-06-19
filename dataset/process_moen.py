import os
from pydoc import describe
import sqlite3
import re
import time
from IPA_dicts import vowels, consonants
import logging

logger = logging.getLogger('process_logger')
f_handler = logging.FileHandler('file.log', 'w', 'utf-8')
logger.setLevel(logging.INFO)
f_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
logger.addHandler(f_handler)


def extract_eraab(word, description):
    eraab_group = re.search(r"^\(([^\(]*)\) *\[?[^\[\(]*\]? *\([^\(]*\)", description)
    if eraab_group == None:
        eraab = None
    else:
        eraab = " ".join(eraab_group.group(1).split())
    transformed_word = add_eraab_to_word(word, eraab)
    if validate_pronounce(transformed_word):
        return transformed_word
    else:
        return None


def add_eraab_to_word(word, eraab):
    if eraab is None:
        return word
    
    if '~' in eraab:
        logger.warning("~ in eraab")
        return ''

    eraab_list = eraab.strip().replace("ء", "ئ").split(" ")
    for part in eraab_list:
        if len(part) > 2:
            logger.warning(f"wrong eraab {eraab} for word {word} in part {part}")
            return ""

    transformed_word = ""
    word_idx = 0
    eraab_idx = 0
    while eraab_idx < len(eraab_list):
        if word_idx >= len(word):
            logger.warning(f"error parsing {word} with {eraab}")
            return ""

        if eraab_list[eraab_idx] == "یا":
            eraab_idx += 2
            continue
        transformed_word += word[word_idx]

        if eraab_list[eraab_idx][0] == word[word_idx]:
            if len(eraab_list[eraab_idx]) == 1:
                pass
            elif eraab_list[eraab_idx][1] in "َُِْ":
                transformed_word += eraab_list[eraab_idx][1]
            elif (
                word_idx + 1 < len(word)
                and eraab_list[eraab_idx][1] == word[word_idx + 1]
            ):
                pass
            else:
                logger.warning(f"wrong eraab {eraab} for word {word}")
                return ""
            eraab_idx += 1

        word_idx += 1
    if word_idx < len(word):
        transformed_word = transformed_word + word[word_idx:]
    return transformed_word


def validate_pronounce(eraab):
    # TODO: add characters that allow 3 samet.
    if not set(eraab).issubset(set(consonants.keys()).union(set(vowels.keys()))):
        logger.warning(f"word {eraab} has non-alphabet characters")
        return False
    samet = 3
    start = True
    if eraab == None or len(eraab) == 0:
        return False
    if eraab[-1] in "َُِ":
        return False
    for ch in eraab:
        if start:
            start = False
            if ch == "آ":
                samet = 0
            continue
        if samet == 0 and ch not in "اَُِآ":
            samet += 1
            continue
        if ch in "آاَوُیِ":
            samet = 0
        else:
            samet += 1
        if samet > 3:
            return False
    return True if samet < 3 else False


def extract_pos(description):
    pos_group = re.search(r'^\(?[^\(]*\)? *\[?[^\[\(]*\]? *\(([^\(]*)\)', description)
    pos = pos_group.group(1) if pos_group is not None else pos_group
    return pos


def extract_IPA(word):
    if word == None:
        return None
    idx = 1
    ipa = consonants[word[0]]
    prev = "a"  # any char except vowels will do.
    while idx < len(word):
        if word[idx] in "اَُِْ":
            ipa += vowels[word[idx]]
        elif prev in "اَُِْ":
            ipa += consonants[word[idx]]
        elif word[idx] in "یو":
            if prev in "وی":
                ipa += consonants[prev] + vowels[word[idx]]
            else:
                ipa += vowels[word[idx]]
        else:
            ipa += consonants[word[idx]]
        prev = word[idx]
        idx += 1
    return ipa


def extract_meaning(description):
    # TODO
    return None


class Database:
    def __init__(self, db_file="moen_parsed.db"):
        """create a database connection to a SQLite database and create table if not exists"""
        self.conn = sqlite3.connect(db_file)
        create_table = """CREATE TABLE IF NOT EXISTS dictionary (
                                        id integer PRIMARY KEY,
                                        word text NOT NULL,
                                        eraab text,
                                        pos text,
                                        IPA text,
                                        meaning text
                                    );"""
        self.cursor = self.conn.cursor()
        self.cursor.execute(create_table)

    def insert(self, word, pos, eraab, IPA, meaning):
        insert_query = """ INSERT INTO dictionary(word, pos, eraab, IPA, meaning)
              VALUES(?,?,?,?,?) """
        self.cursor.execute(insert_query, (word, pos, eraab, IPA, meaning))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

def read_moen(db_file = "moein.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    lookup_word_query = """ SELECT * FROM wordbook """
    cursor.execute(lookup_word_query)
    rows = cursor.fetchall()
    conn.close()
    print(len(rows))
    return rows

def parse_row(row):
    word = row[3]
    description = row[6]
    if " " in word or "‌" in word or "ة" in word:  # space or half space
        return
    if word == None or word == "":
        logger.error(f"row {counter} is empty")
        return
    eraab = extract_eraab(word, description)
    if eraab == None:
        return
    pos = extract_pos(description)
    # meaning = extract_meaning(description)
    meaning = description
    IPA = extract_IPA(eraab)
    db.insert(word, pos, eraab, IPA, meaning)

if __name__ == "__main__":
    # iterate over folders
    start_time = time.time()
    db = Database()
    rows = read_moen()
    counter = 1
    for row in rows:
        counter += 1
        parse_row(row)
        if counter % 100 == 0:
            logger.info(f"added {counter} entries")
    del db
