import sqlite3
from datetime import datetime


DB = "database.db"


def connect():
    return sqlite3.connect(DB)



# ================= INIT =================


def create_table():

    db = connect()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(

        user_id INTEGER PRIMARY KEY,

        city TEXT,

        notifications INTEGER DEFAULT 1

    )
    """)

    db.commit()
    db.close()



def create_reports_table():

    db = connect()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS reports(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        city TEXT,

        status TEXT,

        created TEXT

    )
    """)

    db.commit()
    db.close()



def create_alerts_table():

    db = connect()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS alerts(

        city TEXT PRIMARY KEY,

        message_id INTEGER,

        status TEXT DEFAULT 'no_power'

    )
    """)

    db.commit()
    db.close()



def create_users_table():

    create_table()



# ================= USERS =================


def save_user_city(user_id, city):

    db = connect()
    cur = db.cursor()

    cur.execute("""
    INSERT INTO users(
        user_id,
        city,
        notifications
    )

    VALUES(?,?,1)

    ON CONFLICT(user_id)

    DO UPDATE SET city=excluded.city

    """,
    (
        user_id,
        city
    ))

    db.commit()
    db.close()



def get_user_city(user_id):

    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        SELECT city
        FROM users
        WHERE user_id=?
        """,
        (user_id,)
    )

    row = cur.fetchone()

    db.close()

    return row[0] if row else None



# ================= NOTIFICATIONS =================


def get_notifications(user_id):

    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        SELECT notifications
        FROM users
        WHERE user_id=?
        """,
        (user_id,)
    )

    row = cur.fetchone()

    db.close()

    if row:
        return row[0]

    return 1



def set_notifications(user_id, value):

    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        UPDATE users

        SET notifications=?

        WHERE user_id=?

        """,
        (
            value,
            user_id
        )
    )

    db.commit()
    db.close()



def get_users_by_city(city):

    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        SELECT user_id

        FROM users

        WHERE city=?

        AND notifications=1

        """,
        (city,)
    )

    rows = cur.fetchall()

    db.close()

    return [
        r[0]
        for r in rows
    ]



# ================= REPORTS =================


def save_report(user_id, city, status):

    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        INSERT INTO reports

        VALUES(
            NULL,
            ?,
            ?,
            ?,
            ?
        )

        """,
        (
            user_id,
            city,
            status,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )
        )
    )

    db.commit()
    db.close()



def get_city_stats(city):

    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        SELECT COUNT(*)

        FROM reports

        WHERE city=?

        AND status='no_power'

        """,
        (city,)
    )

    result = cur.fetchone()[0]

    db.close()

    return result



# ================= CITY STATUS =================


def get_city_status(city):

    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        SELECT status, created

        FROM reports

        WHERE city=?

        ORDER BY id DESC

        LIMIT 1

        """,
        (city,)
    )

    row = cur.fetchone()

    db.close()

    return row

def has_report(user_id, city):
    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        SELECT id
        FROM reports
        WHERE user_id=?
        AND city=?
        AND status='no_power'
        """,
        (
            user_id,
            city
        )
    )

    row = cur.fetchone()

    db.close()

    return row is not None
