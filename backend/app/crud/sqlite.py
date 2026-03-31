from __future__ import annotations

import sqlite3
import threading

from app.schemas.alert import Alert, LogEvent
from app.schemas.post import EnrichedPost
from app.schemas.score import RegionScore
from app.crud.base import Store


class SQLiteStore(Store):
    def __init__(self, db_path: str = "ai4mh.db", max_posts: int = 500) -> None:
        self._db_path = db_path
        self._max_posts = max_posts
        self._lock = threading.Lock()
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._db_path, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute("PRAGMA journal_mode=WAL;")
            connection.execute(
                "CREATE TABLE IF NOT EXISTS posts (id TEXT PRIMARY KEY, idx INTEGER, data JSON)"
            )
            connection.execute(
                "CREATE TABLE IF NOT EXISTS scores (region_id TEXT PRIMARY KEY, data JSON)"
            )
            connection.execute(
                "CREATE TABLE IF NOT EXISTS alerts (id TEXT PRIMARY KEY, data JSON)"
            )
            connection.execute(
                "CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, data JSON)"
            )

    def save_posts(self, posts: list[EnrichedPost]) -> None:
        with self._lock:
            with self._connect() as connection:
                row = connection.execute("SELECT MAX(idx) AS max_idx FROM posts").fetchone()
                start = row["max_idx"] or 0
                payload = [
                    (post.id, start + offset + 1, post.model_dump_json())
                    for offset, post in enumerate(reversed(posts))
                ]
                connection.executemany(
                    "INSERT OR REPLACE INTO posts (id, idx, data) VALUES (?, ?, ?)",
                    payload,
                )
                connection.execute(
                    f"DELETE FROM posts WHERE id NOT IN (SELECT id FROM posts ORDER BY idx DESC LIMIT {self._max_posts})"
                )

    def get_posts(self, limit: int | None = None) -> list[EnrichedPost]:
        query = "SELECT data FROM posts ORDER BY idx DESC"
        if limit is not None:
            query = f"{query} LIMIT {limit}"

        with self._connect() as connection:
            rows = connection.execute(query).fetchall()
        return [EnrichedPost.model_validate_json(row["data"]) for row in rows]

    def save_scores(self, scores: list[RegionScore]) -> None:
        with self._lock:
            with self._connect() as connection:
                connection.execute("DELETE FROM scores")
                connection.executemany(
                    "INSERT INTO scores (region_id, data) VALUES (?, ?)",
                    [(score.region_id, score.model_dump_json()) for score in scores],
                )

    def get_scores(self) -> list[RegionScore]:
        with self._connect() as connection:
            rows = connection.execute("SELECT data FROM scores").fetchall()
        scores = [RegionScore.model_validate_json(row["data"]) for row in rows]
        return sorted(scores, key=lambda item: item.crisis_score, reverse=True)

    def save_alerts(self, alerts: list[Alert]) -> None:
        with self._lock:
            with self._connect() as connection:
                connection.execute("DELETE FROM alerts")
                connection.executemany(
                    "INSERT INTO alerts (id, data) VALUES (?, ?)",
                    [(alert.id, alert.model_dump_json()) for alert in alerts],
                )

    def get_alerts(self) -> list[Alert]:
        with self._connect() as connection:
            rows = connection.execute("SELECT data FROM alerts").fetchall()
        return [Alert.model_validate_json(row["data"]) for row in rows]

    def get_alert(self, alert_id: str) -> Alert | None:
        with self._connect() as connection:
            row = connection.execute("SELECT data FROM alerts WHERE id = ?", (alert_id,)).fetchone()
        if row is None:
            return None
        return Alert.model_validate_json(row["data"])

    def update_alert(self, alert: Alert) -> None:
        with self._lock:
            with self._connect() as connection:
                connection.execute(
                    "UPDATE alerts SET data = ? WHERE id = ?",
                    (alert.model_dump_json(), alert.id),
                )

    def append_log(self, event: LogEvent) -> None:
        with self._lock:
            with self._connect() as connection:
                connection.execute("INSERT INTO logs (data) VALUES (?)", (event.model_dump_json(),))

    def get_logs(self, limit: int = 100) -> list[LogEvent]:
        with self._connect() as connection:
            rows = connection.execute(
                f"SELECT data FROM logs ORDER BY id DESC LIMIT {limit}"
            ).fetchall()
        return [LogEvent.model_validate_json(row["data"]) for row in reversed(rows)]
