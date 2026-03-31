from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.alert import Alert, LogEvent
from app.schemas.post import EnrichedPost
from app.schemas.score import RegionScore


class Store(ABC):
    @abstractmethod
    def save_posts(self, posts: list[EnrichedPost]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_posts(self, limit: int | None = None) -> list[EnrichedPost]:
        raise NotImplementedError

    @abstractmethod
    def save_scores(self, scores: list[RegionScore]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_scores(self) -> list[RegionScore]:
        raise NotImplementedError

    @abstractmethod
    def save_alerts(self, alerts: list[Alert]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_alerts(self) -> list[Alert]:
        raise NotImplementedError

    @abstractmethod
    def get_alert(self, alert_id: str) -> Alert | None:
        raise NotImplementedError

    @abstractmethod
    def update_alert(self, alert: Alert) -> None:
        raise NotImplementedError

    @abstractmethod
    def append_log(self, event: LogEvent) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_logs(self, limit: int = 100) -> list[LogEvent]:
        raise NotImplementedError
