import sqlite3
from datetime import datetime

DB_NAME = "ecobuddy.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Users table to store total lifetime points
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            total_points INTEGER DEFAULT 0,
            items_logged INTEGER DEFAULT 0
        )
    """)
    # History table to store item log audit trail
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            item TEXT,
            points_awarded INTEGER,
            timestamp TEXT,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    """)
    conn.commit()
    conn.close()

def add_points(username: str, item: str, points: int = 10) -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Ensure user exists or insert initial row
    cursor.execute("""
        INSERT INTO users (username, total_points, items_logged)
        VALUES (?, ?, 1)
        ON CONFLICT(username) DO UPDATE SET
            total_points = total_points + ?,
            items_logged = items_logged + 1
    """, (username, points, points))
    
    # Insert audit record
    cursor.execute("""
        INSERT INTO logs (username, item, points_awarded, timestamp)
        VALUES (?, ?, ?, ?)
    """, (username, item, points, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    # Retrieve new total
    cursor.execute("SELECT total_points FROM users WHERE username = ?", (username,))
    new_total = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()
    return new_total

def get_user_stats(username: str) -> dict:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT total_points, items_logged FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"total_points": row[0], "items_logged": row[1]}
    return {"total_points": 0, "items_logged": 0}