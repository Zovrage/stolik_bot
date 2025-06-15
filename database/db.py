import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'DataBase.db')


BASE_NAME = DB_PATH

USERS = 'users'
BOOKING = 'bookings'

def create_table():
    with sqlite3.connect(BASE_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {BOOKING} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                time TEXT,
                guests INTEGER,
                preferences TEXT,
                paid INTEGER
            )
        """)

        conn.commit()

