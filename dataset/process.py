#first draft of the code
import os
import sqlite3
import re
import time
from IPA_dicts import vowels, consonants

def process_entry(file):
    with open(file, encoding='utf-8') as f:
        text = f.read()
        word_group = re.search(r'<h1 class="text-justify">([\s\S^<]*)<\/h1>', text)
        if word_group is None:
            print(f'{file} has no word')
            word = word_group
        else:
            word = word_group.group(1)
            if  not (len(word_group.groups()) == 1):
                print(f'{file} more than one word')
        des_group = re.search(r'<div class="content text-justify">([\s\S]*)<\/div>', text)
        if des_group is None:
            description = des_group
            print(f'{file} has no description')
        else:
            description = des_group.group(1).strip()
            if not (len(des_group.groups()) == 1):
                print(f'{file} more than one description')

    return (word, description)

def extract_eraab(word, description):
    eraab_group = re.search(r'^\[([^\]]*)\]', description)
    eraab = eraab_group.group(1).strip() if eraab_group is not None else eraab_group
    transformed_word = add_eraab_to_word(word, eraab)

    if validate_pronounce(transformed_word):
        return transformed_word
    else:
        return None

def add_eraab_to_word(word, eraab):
    if eraab is None: return word

    eraab_list = eraab.strip().replace('ء', 'ئ').split(' ')
    for part in eraab_list:
        if len(part) != 2 and part != '/':
            print(f'wrong eraab {eraab} for word {word} in part {part}')
            return ''
    transformed_word = ''
    word_idx = 0
    eraab_idx = 0
    while eraab_idx < len(eraab_list):
        if word_idx >= len(word):
            print(f'erorr parsing {word} with {eraab}')
            return ''

        if eraab_list[eraab_idx] == '/':
            eraab_idx += 2
            continue
        transformed_word += word[word_idx]

        if eraab_list[eraab_idx][0] == word[word_idx]:
            if eraab_list[eraab_idx][1] in 'َُِْ':
                transformed_word += eraab_list[eraab_idx][1]
            elif word_idx + 1 < len(word) and eraab_list[eraab_idx][1] == word[word_idx + 1]:
                pass
            else:
                print(f'wrong eraab {eraab} for word {word}')
                return ''
            eraab_idx += 1

        word_idx += 1
    if word_idx < len(word):
        transformed_word = (transformed_word + word[word_idx:]) 
    return transformed_word 

def validate_pronounce(eraab):
    #TODO: add characters that allow 3 samet.
    samet = 3
    start = True
    for ch in eraab:
        if start:
            start = False
            if ch == 'آ':
                samet = 0
            continue
        if samet == 0 and ch not in "اَُِآ":
            samet += 1
            continue
        if ch in 'آاَوُیِ':
            samet = 0
        else:
            samet += 1
        if samet > 3:
            return False
    return True if samet < 3 else False

def extract_pos(description):
    pos_group = re.search(r'<span style="color:orange">\((.*)\)</span>', description)
    # assert (len(pos_group.groups()) == 1)
    pos = pos_group.group(1) if pos_group is not None else pos_group
    return pos

def extract_IPA(word):
    if word == None:
        return None
    idx = 1
    ipa = consonants[word[0]]
    prev = "a" # any char except vowels will do.
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
    #TODO
    return None

class Database:
    def __init__(self, db_file = 'dehkhoda.db'):
        """ create a database connection to a SQLite database and create table if not exists """
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
        insert_query = ''' INSERT INTO dictionary(word, pos, eraab, IPA, meaning)
              VALUES(?,?,?,?,?) '''
        self.cursor.execute(insert_query, (word, pos, eraab, IPA, meaning))
        self.conn.commit()


    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
#iterate over folders
    start_time = time.time()
    counter = 1 
    db = Database()
    for i in range(35):
        for file in os.listdir(f'dehkhoda/{i}/'):
            counter += 1
            if counter % 100 == 0 : print(counter)
            word, description = process_entry(f'dehkhoda/{i}/{file}')
            if ' ' in word or '‌' in word or 'ة' in word: #space or half space
                continue
            if word == None or word == '':
                print(f'{file} is empty')
            pos = extract_pos(description)
            eraab = extract_eraab(word, description)
            # meaning = extract_meaning(description)
            meaning = description
            IPA = extract_IPA(eraab)
            db.insert(word, pos, eraab, IPA, meaning)
        print("+"*100)
        print(f"end of file{i} in {time.time() - start_time} seconds")
        print(f"added {counter} words to db")

    del db
