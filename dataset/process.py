#first draft of the code
import os
import sqlite3
import re
import time


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
    # assert (len(eraab_group.groups()) == 1)
    eraab = eraab_group.group(1) if eraab_group is not None else eraab_group
    return eraab

def extract_pos(description):
    pos_group = re.search(r'<span style="color:orange">\((.*)\)</span>', description)
    # assert (len(pos_group.groups()) == 1)
    pos = pos_group.group(1) if pos_group is not None else pos_group
    return pos

def extract_meaning(description):
    #TODO
    return(None, None)

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

    db = Database()
    for i in range(35):
        for file in os.listdir(f'dehkhoda/{i}/'):
            # print(file)
            word, description = process_entry(f'dehkhoda/{i}/{file}')
            if word == None or word == '':
                print(f'{file} is empty')
            pos = extract_pos(description)
            eraab = extract_eraab(word, description)
            # meaning = extract_meaning(description)
            meaning = description
            IPA = None
            db.insert(word, pos, eraab, IPA, meaning)
        print(f"end of file{i} in {time.time() - start_time} seconds")

    del db
