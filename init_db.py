import sqlite3
import os

DB_PATH = "test.db"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

cur.execute("INSERT INTO users (username, password) VALUES ('alice', 'password123')")
cur.execute("INSERT INTO users (username, password) VALUES ('bob', 'qwerty')")
conn.commit()
conn.close()

print("Initialized test.db")