"""
AI4MH — SQLite Storage Backend

Persistent implementation of the Store interface using SQLite.
Uses PRAGMA journal_mode=WAL for better concurrency.
"""

from __future__ import annotations

import json
import sqlite3
import threading
from typing import List, Optional

from models.post import EnrichedPost
from models.score import RegionScore
from models.alert import Alert, LogEvent
from storage.base import Store


class SQLiteStore(Store):
    """Persistent storage using SQLite with JSON columns."""

    def __init__(self, db_path: str = "ai4mh.db", max_posts: int = 500) -> None:
        self._max_posts = max_posts
        self._db_path = db_path
        self._lock = threading.Lock()  # Write lock to prevent DB locking issues
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._get_conn() as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute(
                "CREATE TABLE IF NOT EXISTS posts (id TEXT PRIMARY KEY, idx INTEGER, data JSON)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS scores (region_id TEXT PRIMARY KEY, data JSON)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS alerts (id TEXT PRIMARY KEY, data JSON)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, data JSON)"
            )

    # ------------------------------------------------------------------ posts
    def save_posts(self, posts: List[EnrichedPost]) -> None:
        with self._lock:
            with self._get_conn() as conn:
                # get current max idx to prepend
                cur = conn.execute("SELECT MAX(idx) as m FROM posts")
                row = cur.fetchone()
                current_max = row["m"] if row and row["m"] is not None else 0
                
                # Prepend posts by assigning higher indexes
                to_insert = []
                for i, p in enumerate(reversed(posts)):
                    to_insert.append((p.id, current_max + i + 1, p.model_dump_json()))
                
                conn.executemany(
                    "INSERT OR REPLACE INTO posts (id, idx, data) VALUES (?, ?, ?)",
                    to_insert
                )
                
                # Trim to max_posts
                conn.execute(
                    f"DELETE FROM posts WHERE id NOT IN (SELECT id FROM posts ORDER BY idx DESC LIMIT {self._max_posts})"
                )

    def get_posts(self, limit: Optional[int] = None) -> List[EnrichedPost]:
        query = "SELECT data FROM posts ORDER BY idx DESC"
        if limit is not None:
            query += f" LIMIT {limit}"
        
        with self._get_conn() as conn:
            rows = conn.execute(query).fetchall()
            return [EnrichedPost.model_validate_json(row["data"]) for row in rows]

    # ----------------------------------------------------------------- scores
    def save_scores(self, scores: List[RegionScore]) -> None:
        with self._lock:
            with self._get_conn() as conn:
                conn.execute("DELETE FROM scores")
                to_insert = [(s.region_id, s.model_dump_json()) for s in scores]
                conn.executemany("INSERT INTO scores (region_id, data) VALUES (?, ?)", to_insert)

    def get_scores(self) -> List[RegionScore]:
        with self._get_conn() as conn:
            rows = conn.execute("SELECT data FROM scores").fetchall()
            # Order originally maintained by insertion/score, but here we just return them.
            # Real sorting usually happens at the application/API layer if needed, 
            # though the pipeline guarantees it passes sorted.
            scores = [RegionScore.model_validate_json(row["data"]) for row in rows]
            # Maintain the sorting by crisis_score descending
            return sorted(scores, key=lambda s: s.crisis_score, reverse=True)

    # ----------------------------------------------------------------- alerts
    def save_alerts(self, alerts: List[Alert]) -> None:
        with self._lock:
            with self._get_conn() as conn:
                conn.execute("DELETE FROM alerts")
                to_insert = [(a.id, a.model_dump_json()) for a in alerts]
                conn.executemany("INSERT INTO alerts (id, data) VALUES (?, ?)", to_insert)

    def get_alerts(self) -> List[Alert]:
        with self._get_conn() as conn:
            rows = conn.execute("SELECT data FROM alerts").fetchall()
            return [Alert.model_validate_json(row["data"]) for row in rows]

    def get_alert(self, alert_id: str) -> Optional[Alert]:
        with self._get_conn() as conn:
            row = conn.execute("SELECT data FROM alerts WHERE id=?", (alert_id,)).fetchone()
            if row:
                return Alert.model_validate_json(row["data"])
        return None

    def update_alert(self, alert: Alert) -> None:
        with self._lock:
            with self._get_conn() as conn:
                conn.execute("UPDATE alerts SET data=? WHERE id=?", (alert.model_dump_json(), alert.id))

    # ------------------------------------------------------------------- logs
    def append_log(self, event: LogEvent) -> None:
        with self._lock:
            with self._get_conn() as conn:
                conn.execute("INSERT INTO logs (data) VALUES (?)", (event.model_dump_json(),))

    def get_logs(self, limit: int = 100) -> List[LogEvent]:
        with self._get_conn() as conn:
            rows = conn.execute(f"SELECT data FROM logs ORDER BY id DESC LIMIT {limit}").fetchall()
            # return in chronological order (oldest first if desired, or newest first?)
            # The memory store returns `self._logs[-limit:]` which is chronological.
            # query gets newest first, so we reverse it.
            return [LogEvent.model_validate_json(row["data"]) for row in reversed(rows)]
