import sqlite3


DB_NAME = "messages.db"


def connect():
    return sqlite3.connect(DB_NAME)


# ------------------------
# MESSAGES
# ------------------------

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
    """, (
        user_id,
        text,
        city,
        district,
        problem,
        duration
    ))

    conn.commit()
    conn.close()


# ------------------------
# REPORTS
# ------------------------

def create_reports_table():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT UNIQUE,
        city TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_report(user_id, city, status):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO reports(user_id, city, status)
    VALUES (?, ?, ?)
    ON CONFLICT(user_id)
    DO UPDATE SET
        city=excluded.city,
        status=excluded.status,
        created_at=CURRENT_TIMESTAMP
    """, (
        user_id,
        city,
        status
    ))

    conn.commit()
    conn.close()


def get_city_stats(city):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM reports
    WHERE city=?
    AND status='no_power'
    """, (city,))

    result = cursor.fetchone()[0]

    conn.close()

    return result


def get_power_ok_count(city):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM reports
    WHERE city=?
    AND status='power_ok'
    """, (city,))

    result = cursor.fetchone()[0]

    conn.close()

    return result


# ------------------------
# ALERTS
# ------------------------

def create_alerts_table():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        city TEXT PRIMARY KEY,
        message_id INTEGER
    )
    """)

    conn.commit()
    conn.close()


def get_alert(city):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT message_id
    FROM alerts
    WHERE city=?
    """, (city,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


def save_alert(city, message_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO alerts
    (
        city,
        message_id
    )
    VALUES (?, ?)
    """, (
        city,
        message_id
    ))

    conn.commit()
    conn.close()


# ------------------------
# CITY STATUS
# ------------------------

def create_city_status_table():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS city_status(
        city TEXT PRIMARY KEY,
        status TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def set_city_status(city, status):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO city_status
    (
        city,
        status,
        updated_at
    )
    VALUES
    (
        ?,
        ?,
        CURRENT_TIMESTAMP
    )
    """, (
        city,
        status
    ))

    conn.commit()
    conn.close()


def get_city_status(city):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT status
    FROM city_status
    WHERE city=?
    """, (city,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


# ------------------------
# POWER EVENTS
# ------------------------

def create_power_events_table():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS power_events (
        city TEXT PRIMARY KEY,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def set_power_start(city):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO power_events
    (
        city,
        started_at
    )
    VALUES
    (
        ?,
        CURRENT_TIMESTAMP
    )
    """, (city,))

    conn.commit()
    conn.close()


def get_power_start(city):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT started_at
    FROM power_events
    WHERE city=?
    """, (city,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None
def create_users_table():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            telegram_id INTEGER UNIQUE,

            city TEXT,

            notifications INTEGER DEFAULT 1

        )
    """)

    conn.commit()
    conn.close()

def save_user_city(telegram_id, city):

    conn = connect()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (telegram_id, city)
        VALUES (?, ?)

        ON CONFLICT(telegram_id)
        DO UPDATE SET city=excluded.city
        """,
        (
            telegram_id,
            city
        )
    )

    conn.commit()
    conn.close()



def get_user_city(telegram_id):

    conn = connect()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT city
        FROM users
        WHERE telegram_id=?
        """,
        (telegram_id,)
    )

    result = cursor.fetchone()

    conn.close()


    if result:
        return result[0]

    return None



def get_city_users(city):

    conn = connect()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT telegram_id
        FROM users
        WHERE city=?
        AND notifications=1
        """,
        (city,)
    )

    users = cursor.fetchall()

    conn.close()

    return [
        user[0]
        for user in users
    ]
    
def get_notifications(telegram_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT notifications
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return 1



def set_notifications(telegram_id, value):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET notifications = ?
        WHERE telegram_id = ?
        """,
        (
            value,
            telegram_id
        )
    )

    conn.commit()
    conn.close()

def get_all_statuses():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            city,
            status,
            updated_at
        FROM city_status
    """)

    rows = cursor.fetchall()

    conn.close()


    result = []

    for row in rows:

        city = row[0]
        status = row[1]
        updated = row[2]


        result.append({

            "name": city,

            "statusCode":
                "red" if status == "no_power"
                else "green",

            "status":
                "Нет света" if status == "no_power"
                else "Есть свет",

            "updated": updated

        })


    return result
