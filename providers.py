import sqlite3
from contextlib import contextmanager
from time import time

from app.config import settings


@contextmanager
def db():
    conn = sqlite3.connect(settings.database_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS cooldowns (
            provider TEXT PRIMARY KEY,
            until_ts REAL NOT NULL,
            reason TEXT NOT NULL
        )
        """)


def set_cooldown(provider: str, seconds: int, reason: str) -> None:
    until_ts = time() + seconds
    with db() as conn:
        conn.execute(
            "REPLACE INTO cooldowns(provider, until_ts, reason) VALUES (?, ?, ?)",
            (provider, until_ts, reason),
        )


def is_on_cooldown(provider: str) -> tuple[bool, int, str]:
    with db() as conn:
        row = conn.execute(
            "SELECT until_ts, reason FROM cooldowns WHERE provider = ?",
            (provider,),
        ).fetchone()

    if not row:
        return False, 0, ""

    remaining = int(row["until_ts"] - time())
    if remaining <= 0:
        return False, 0, ""
    return True, remaining, row["reason"]


def reset_cooldowns() -> None:
    with db() as conn:
        conn.execute("DELETE FROM cooldowns")


def list_cooldowns() -> list[dict]:
    with db() as conn:
        rows = conn.execute("SELECT provider, until_ts, reason FROM cooldowns").fetchall()

    now = time()
    return [
        {
            "provider": r["provider"],
            "remaining_seconds": max(0, int(r["until_ts"] - now)),
            "reason": r["reason"],
        }
        for r in rows
        if r["until_ts"] > now
    ]
