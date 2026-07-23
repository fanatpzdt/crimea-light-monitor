import sqlite3


def connect():
    return sqlite3.connect("messages.db")


def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_message(text):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (text) VALUES (?)",
        (text,)
    )

    conn.commit()
    conn.close()
