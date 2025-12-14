import sqlite3
from pathlib import Path
from typing import List, Tuple

DB_PATH = Path(__file__).parent / "memory.db"

def _get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def append_to_session(session_id: str, role: str, content: str):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO conversations (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )
    conn.commit()
    conn.close()

def get_session_context(session_id: str, limit: int = 10) -> str:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT role, content
        FROM conversations
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (session_id, limit))
    rows = cur.fetchall()
    conn.close()

    rows.reverse()
    context = []
    for role, content in rows:
        prefix = "User" if role == "user" else "Assistant"
        context.append(f"{prefix}: {content}")

    return "\n".join(context)
