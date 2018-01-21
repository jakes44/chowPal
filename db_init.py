# Init sqlite db
import sqlite3

# Main init function
def db_init():
    # Create and connect to db
    db = sqlite3.connect('DB/chow.db')
    c = db.cursor()

    # Schema stuff 
    c.execute('''CREATE TABLE IF NOT EXISTS user_profile (
                uid INTEGER,
                dietary_restriction TEXT)
                ''')

    c.execute('''CREATE TABLE IF NOT EXISTS choices (
                uid INTEGER,
                did INTEGER,
                cid INTEGER, 
                point REAL,
                rating REAL )''')

    c.execute('''CREATE TABLE IF NOT EXISTS co_data (
                did INTEGER,
                blurb TEXT, 
                health_info BLOB )''')

    db.commit()
    db.close()

if __name__ == '__main__':
    db_init()
