import sqlite3
import hashlib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'database', 'users.db')

def sifrele(sifre):
    return hashlib.sha256(sifre.encode()).hexdigest()

def kullanici_ekle(email, sifre):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, sifrele(sifre)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def giris_dogrula(email, sifre):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email=?", (email,))
    row = cursor.fetchone()
    conn.close()
    return row and row[0] == sifrele(sifre)
