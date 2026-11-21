"""Small, inspectable SQLite memory layer for the public Nova demo."""
from __future__ import annotations

import sqlite3
import time
from pathlib import Path


class MemoryStore:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL CHECK(length(text) BETWEEN 1 AND 2000),
                created_at REAL NOT NULL
            )""")

    def _connect(self):
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        return db

    def add(self, text: str) -> dict:
        text = " ".join(str(text).split())
        if not 1 <= len(text) <= 2000:
            raise ValueError("Memory must be between 1 and 2,000 characters.")
        with self._connect() as db:
            cursor = db.execute("INSERT INTO memories(text, created_at) VALUES(?, ?)", (text, time.time()))
            memory_id = cursor.lastrowid
        # Leave the transaction before opening the independent read connection.
        return self.get(memory_id)

    def get(self, memory_id: int) -> dict:
        with self._connect() as db:
            row = db.execute("SELECT id, text, created_at FROM memories WHERE id=?", (memory_id,)).fetchone()
        if row is None:
            raise KeyError(memory_id)
        return dict(row)

    def recent(self, limit: int = 20) -> list[dict]:
        limit = max(1, min(int(limit), 100))
        with self._connect() as db:
            rows = db.execute("SELECT id, text, created_at FROM memories ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(row) for row in rows]

    def search(self, query: str, limit: int = 5) -> list[dict]:
        query = " ".join(str(query).split())
        if not query:
            return []
        with self._connect() as db:
            rows = db.execute("SELECT id, text, created_at FROM memories WHERE text LIKE ? ORDER BY id DESC LIMIT ?", (f"%{query}%", max(1, min(int(limit), 20)))).fetchall()
        return [dict(row) for row in rows]
