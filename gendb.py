import sqlite3

db = sqlite3.connect('temp.db')

cursor = db.cursor()

cursor.execute('''
    CREATE TABLE messages(id INTEGER PRIMARY KEY, msg_id INTEGER, name TEXT,
                       topic TEXT, nick TEXT, handle TEXT, body TEXT)
''')
db.commit()
