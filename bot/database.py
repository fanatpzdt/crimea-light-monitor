import sqlite3


def connect():
    return sqlite3.connect("database.db")


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
        status TEXT
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



def save_city(user_id, city):

    db=connect()
    cur=db.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO users
    VALUES(?,?)
    """,(user_id,city))

    db.commit()
    db.close()



def get_city(user_id):

    db=connect()
    cur=db.cursor()

    cur.execute(
        "SELECT city FROM users WHERE user_id=?",
        (user_id,)
    )

    row=cur.fetchone()

    db.close()

    return row[0] if row else None



def save_report(user_id,city,status):

    db=connect()
    cur=db.cursor()

    cur.execute("""
    INSERT INTO reports
    VALUES(NULL,?,?,?)
    """,
    (
        user_id,
        city,
        status
    ))

    db.commit()
    db.close()



def count_no_power(city):

    db=connect()
    cur=db.cursor()


    cur.execute("""
    SELECT COUNT(*)
    FROM reports
    WHERE city=?
    AND status='no_power'
    """,
    (city,))


    result=cur.fetchone()[0]


    db.close()

    return result
