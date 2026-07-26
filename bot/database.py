import sqlite3


DB_NAME = "database.db"


def connect():
    return sqlite3.connect(DB_NAME)



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
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        message_id INTEGER
    )
    """)

    db.commit()
    db.close()



# Совместимость с твоим main.py

def create_users_table():
    create_table()


def create_city_status_table():
    pass


def create_power_events_table():
    pass



# -------------------------
# Пользователи
# -------------------------


def save_user_city(user_id, city):

    db = connect()
    cur = db.cursor()


    cur.execute(
        """
        INSERT INTO users(user_id, city, notifications)
        VALUES(?,?,1)

        ON CONFLICT(user_id)
        DO UPDATE SET city=excluded.city
        """,
        (
            user_id,
            city
        )
    )


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


    if row:
        return row[0]

    return None



# -------------------------
# Уведомления
# -------------------------


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



# -------------------------
# Отчёты
# -------------------------


def save_report(user_id, city, status):

    db = connect()
    cur = db.cursor()


    cur.execute(
        """
        INSERT INTO reports(
            user_id,
            city,
            status
        )
        VALUES(?,?,?)
        """,
        (
            user_id,
            city,
            status
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


    count = cur.fetchone()[0]


    db.close()


    return count



def get_power_ok_count(city):

    db = connect()
    cur = db.cursor()


    cur.execute(
        """
        SELECT COUNT(*)
        FROM reports
        WHERE city=?
        AND status='power_ok'
        """,
        (city,)
    )


    count = cur.fetchone()[0]


    db.close()

    return count



# -------------------------
# Статусы
# -------------------------


def set_city_status(city,status):
    pass


def set_power_start(city):
    pass



# -------------------------
# Канал
# -------------------------


def get_alert(city):

    db = connect()
    cur = db.cursor()


    cur.execute(
        """
        SELECT message_id
        FROM alerts
        WHERE city=?
        """,
        (city,)
    )


    row = cur.fetchone()


    db.close()


    if row:
        return row[0]

    return None



def save_alert(city,message_id):

    db = connect()
    cur = db.cursor()


    cur.execute(
        """
        INSERT OR REPLACE INTO alerts
        VALUES(?,?)
        """,
        (
            city,
            message_id
        )
    )


    db.commit()
    db.close()
