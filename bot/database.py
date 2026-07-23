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

def save_report(user_id, city, status):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT id 
    FROM reports
    WHERE user_id = ?
    """,
    (user_id,))


    existing = cursor.fetchone()


    if existing:

        cursor.execute("""
        UPDATE reports
        SET city = ?,
            status = ?,
            created_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
        """,
        (
            city,
            status,
            user_id
        ))

    else:

        cursor.execute("""
        INSERT INTO reports
        (
            user_id,
            city,
            status
        )
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            city,
            status
        ))


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
def get_city_stats(city):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT COUNT(*)
    FROM reports
    WHERE city = ?
    AND status = 'no_power'
    """,
    (city,))


    result = cursor.fetchone()[0]


    conn.close()


    return result
