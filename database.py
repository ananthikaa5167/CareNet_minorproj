import sqlite3

DB_NAME = "carenet.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


# ---------- CREATE TABLE ----------
def init_case_table():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lat REAL,
            lon REAL,
            condition TEXT,
            time_delay INTEGER,
            priority REAL,
            assigned_ngo TEXT,
            assigned_volunteer TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------- INSERT CASE ----------
def insert_case(lat, lon, condition, time_delay, priority, ngo, status):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO cases
        (lat, lon, condition, time_delay, priority, assigned_ngo, assigned_volunteer, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (lat, lon, condition, time_delay, priority, ngo, None, status))

    conn.commit()
    conn.close()


# ---------- FETCH ----------
def fetch_cases():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM cases")
    data = c.fetchall()

    conn.close()
    return data


# ---------- ASSIGN VOLUNTEER ----------
def assign_volunteer(case_id, volunteer_name):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        UPDATE cases
        SET assigned_volunteer = ?
        WHERE id = ?
    """, (volunteer_name, case_id))

    conn.commit()
    conn.close()


# ---------- UPDATE STATUS ----------
def update_case_status(case_id, status):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        UPDATE cases
        SET status = ?
        WHERE id = ?
    """, (status, case_id))

    conn.commit()
    conn.close()