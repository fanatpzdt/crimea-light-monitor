import sqlite3


def connect():
    return sqlite3.connect("messages.db")


def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        text TEXT,
        city TEXT,
        district TEXT,
        problem TEXT,
        duration TEXT,
        status TEXT DEFAULT 'new',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_message(
    user_id,
    text,
    city=None,
    district=None,
    problem=None,
    duration=None
):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO messages
    (
        user_id,
        text,
        city,
        district,
        problem,
        duration
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        user_id,
        text,
        city,
        district,
        problem,
        duration
    ))

    conn.commit()
    conn.close()
def create_reports_table():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        city TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
