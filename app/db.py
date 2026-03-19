import sqlite3
import os


def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables(app):
    db_path = os.path.join(app.instance_path, "students.db")
    conn = get_db_connection(db_path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            standard TEXT NOT NULL,
            division TEXT NOT NULL,
            roll_no INTEGER NOT NULL,
            user_id INTEGER,
            UNIQUE(user_id, standard, division, roll_no),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()