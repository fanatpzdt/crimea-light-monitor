import sqlite3


DB_NAME = "database.db"


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():

    db = connect()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        city TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS reports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        city TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS alerts(
        city TEXT PRIMARY KEY,
        message_id INTEGER
    )
    """)

    db.commit()
    db.close()


# ---------- USERS ----------

def save_city(user_id, city):

    db = connect()
    cur = db.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO users(user_id, city)
    VALUES(?,?)
    """, (user_id, city))

    db.commit()
    db.close()


def get_city(user_id):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT city FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cur.fetchone()

    db.close()

    return row[0] if row else None


# ---------- REPORTS ----------

def save_report(user_id, city, status):

    db = connect()
    cur = db.cursor()

    cur.execute("""
    INSERT INTO reports(user_id, city, status)
    VALUES(?,?,?)
    """, (
        user_id,
        city,
        status
    ))

    db.commit()
    db.close()


def count_no_power(city):

    db = connect()
    cur = db.cursor()

    cur.execute("""
    SELECT COUNT(DISTINCT user_id)
    FROM reports
    WHERE city=?
    AND status='no_power'
    """, (city,))

    count = cur.fetchone()[0]

    db.close()

    return count


# ---------- ALERTS ----------

def get_alert(city):

    db = connect()
    cur = db.cursor()

    cur.execute("""
    SELECT message_id
    FROM alerts
    WHERE city=?
    """, (city,))

    row = cur.fetchone()

    db.close()

    return row[0] if row else None


def save_alert(city, message_id):

    db = connect()
    cur = db.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO alerts(city, message_id)
    VALUES(?,?)
    """, (
        city,
        message_id
    ))

    db.commit()
    db.close()


def delete_alert(city):

    db = connect()
    cur = db.cursor()

    cur.execute("""
    DELETE FROM alerts
    WHERE city=?
    """, (city,))

    db.commit()
    db.close()
