"""
AI4MH — In-Memory Storage Backend

Thread-safe in-process implementation of the Store interface.
All data is lost on process restart; no external dependencies required.
Replace with a Redis or SQLite backend by implementing ``storage.base.Store``.
"""

from __future__ import annotations

import threading
from typing import Dict, List, Optional

from models.post import EnrichedPost
from models.score import RegionScore
from models.alert import Alert, LogEvent
from storage.base import Store


class MemoryStore(Store):
    """Volatile in-memory storage for posts, scores, alerts, and log events."""

    def __init__(self, max_posts: int = 500) -> None:
        self._max_posts = max_posts
        self._lock = threading.Lock()

        self._posts: List[EnrichedPost] = []
        self._scores: List[RegionScore] = []
        self._alerts: List[Alert] = []
        self._logs: List[LogEvent] = []

    # ------------------------------------------------------------------ posts
    def save_posts(self, posts: List[EnrichedPost]) -> None:
        """Prepend *posts* and trim to the configured cap."""
        with self._lock:
            self._posts = (posts + self._posts)[: self._max_posts]

    def get_posts(self, limit: Optional[int] = None) -> List[EnrichedPost]:
        with self._lock:
            data = list(self._posts)
        return data[:limit] if limit is not None else data

    # ----------------------------------------------------------------- scores
    def save_scores(self, scores: List[RegionScore]) -> None:
        with self._lock:
            self._scores = list(scores)

    def get_scores(self) -> List[RegionScore]:
        with self._lock:
            return list(self._scores)

    # ----------------------------------------------------------------- alerts
    def save_alerts(self, alerts: List[Alert]) -> None:
        with self._lock:
            self._alerts = list(alerts)

    def get_alerts(self) -> List[Alert]:
        with self._lock:
            return list(self._alerts)

    def get_alert(self, alert_id: str) -> Optional[Alert]:
        with self._lock:
            for alert in self._alerts:
                if alert.id == alert_id:
                    return alert
        return None

    def update_alert(self, alert: Alert) -> None:
        with self._lock:
            for i, existing in enumerate(self._alerts):
                if existing.id == alert.id:
                    self._alerts[i] = alert
                    return

    # ------------------------------------------------------------------- logs
    def append_log(self, event: LogEvent) -> None:
        with self._lock:
            self._logs.append(event)

    def get_logs(self, limit: int = 100) -> List[LogEvent]:
        with self._lock:
            return list(self._logs[-limit:])
