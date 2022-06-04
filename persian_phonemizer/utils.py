import sqlite3
import re

class Database:
    def __init__(self, db_file="dehkhoda.db"):
        """create a database connection to a SQLite database and create table if not exists"""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def lookup_word(self, word):
        lookup_word_query = """ SELECT * FROM dictionary WHERE word = ? """
        self.cursor.execute(lookup_word_query, (word,))
        rows = self.cursor.fetchall()
        return rows

    def __del__(self):
        self.conn.close()

def valid_word(word):
    persian_alpha_codepoints = '\u0621-\u0628\u062A-\u063A\u0641-\u0642\u0644-\u0648\u064E-\u0651\u0655\u067E\u0686\u0698\u06A9\u06AF\u06BE\u06CC'
    result = re.search(f'^[{persian_alpha_codepoints}]*$', word)
    return result