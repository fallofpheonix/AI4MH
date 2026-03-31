from __future__ import annotations

import threading

from app.crud.base import Store
from app.schemas.alert import Alert, LogEvent
from app.schemas.post import EnrichedPost
from app.schemas.score import RegionScore


class MemoryStore(Store):
    def __init__(self, max_posts: int = 500) -> None:
        self._max_posts = max_posts
        self._lock = threading.Lock()
        self._posts: list[EnrichedPost] = []
        self._scores: list[RegionScore] = []
        self._alerts: list[Alert] = []
        self._logs: list[LogEvent] = []

    def save_posts(self, posts: list[EnrichedPost]) -> None:
        with self._lock:
            self._posts = (posts + self._posts)[: self._max_posts]

    def get_posts(self, limit: int | None = None) -> list[EnrichedPost]:
        with self._lock:
            snapshot = list(self._posts)
        if limit is None:
            return snapshot
        return snapshot[:limit]

    def save_scores(self, scores: list[RegionScore]) -> None:
        with self._lock:
            self._scores = list(scores)

    def get_scores(self) -> list[RegionScore]:
        with self._lock:
            return list(self._scores)

    def save_alerts(self, alerts: list[Alert]) -> None:
        with self._lock:
            self._alerts = list(alerts)

    def get_alerts(self) -> list[Alert]:
        with self._lock:
            return list(self._alerts)

    def get_alert(self, alert_id: str) -> Alert | None:
        with self._lock:
            return next((item for item in self._alerts if item.id == alert_id), None)

    def update_alert(self, alert: Alert) -> None:
        with self._lock:
            for index, current in enumerate(self._alerts):
                if current.id == alert.id:
                    self._alerts[index] = alert
                    break

    def append_log(self, event: LogEvent) -> None:
        with self._lock:
            self._logs.append(event)

    def get_logs(self, limit: int = 100) -> list[LogEvent]:
        with self._lock:
            return list(self._logs[-limit:])
