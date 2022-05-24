#first draft of the code
import os
import sqlite3

def process_entry(file):
    #TODO
    return (None, None)

def extract_IPA(word, description):
    #TODO
    return(None, None)

def extract_pos(description):
    #TODO
    return(None, None)

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
                                        pos text,
                                        IPA text,
                                        meaning text
                                    );"""
        self.cursor = self.conn.cursor()
        self.cursor.execute(create_table)
    
    def insert(self, word, pos, IPA, meaning):
        insert_query = ''' INSERT INTO dictionary(word, pos, IPA, meaning)
              VALUES(?,?,?,?) '''
        self.cursor.execute(insert_query, (word, pos, IPA, meaning))
        self.conn.commit()


    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
#iterate over folders
    db = Database()
    for i in range(35):
      for file in os.listdir(f'dehkhoda/{i}/'):

          word, description = process_entry(file)
          IPA = exctract_IPA(word, description)
          pos = exctract_pos(description)
          meaning = extract_meaning(description)

          db.insert(word, pos, IPA, meaning)

    del db
