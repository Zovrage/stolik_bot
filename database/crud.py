import sqlite3
from database.db import BASE_NAME


def add_booking(user_id, date, time, guests, preferences):
    conn = sqlite3.connect(BASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookings (user_id, date, time, guests, preferences)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, date, time, guests, preferences))
    conn.commit()
    conn.close()

def get_user_bookings(user_id):
    conn = sqlite3.connect(BASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE user_id = ?", (user_id,))
    bookings = cursor.fetchall()
    conn.close()
    return bookings

def cancel_booking(user_id):
    conn = sqlite3.connect(BASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()



def is_time_available(date: str, time: str) -> bool:
    conn = sqlite3.connect(BASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM bookings WHERE date = ? AND time = ?', (date, time))
    count = cursor.fetchone()[0]
    conn.close()
    return count < 5