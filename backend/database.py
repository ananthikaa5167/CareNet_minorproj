import sqlite3

DB_NAME = "careNet.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY,
        latitude REAL,
        longitude REAL,
        condition TEXT,
        priority INTEGER,
        assigned_ngo TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()
