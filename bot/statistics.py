from database import connect


def get_city_count(city):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM reports
    WHERE city = ?
    AND status = 'no_power'
    """, (city,))

    count = cursor.fetchone()[0]

    conn.close()

    return count
