"""
AI4MH — Abstract Storage Interface

Defines the contract that all storage backends must implement.
Swap the concrete implementation (memory, Redis, SQLite, …) by
changing only which class is instantiated in main.py.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from models.post import EnrichedPost
from models.score import RegionScore
from models.alert import Alert, LogEvent


class Store(ABC):
    """Abstract base class for the AI4MH storage layer."""

    # ------------------------------------------------------------------ posts
    @abstractmethod
    def save_posts(self, posts: List[EnrichedPost]) -> None:
        """Prepend *posts* to the store, honouring the configured cap."""

    @abstractmethod
    def get_posts(self, limit: Optional[int] = None) -> List[EnrichedPost]:
        """Return stored posts, most-recent first."""

    # ----------------------------------------------------------------- scores
    @abstractmethod
    def save_scores(self, scores: List[RegionScore]) -> None:
        """Replace the current region-score snapshot."""

    @abstractmethod
    def get_scores(self) -> List[RegionScore]:
        """Return the current region-score snapshot."""

    # ----------------------------------------------------------------- alerts
    @abstractmethod
    def save_alerts(self, alerts: List[Alert]) -> None:
        """Overwrite the active alert list."""

    @abstractmethod
    def get_alerts(self) -> List[Alert]:
        """Return the current alert list."""

    @abstractmethod
    def get_alert(self, alert_id: str) -> Optional[Alert]:
        """Return a single alert by ID, or None if not found."""

    @abstractmethod
    def update_alert(self, alert: Alert) -> None:
        """Persist an updated alert record."""

    # ------------------------------------------------------------------- logs
    @abstractmethod
    def append_log(self, event: LogEvent) -> None:
        """Append a log entry."""

    @abstractmethod
    def get_logs(self, limit: int = 100) -> List[LogEvent]:
        """Return the *limit* most-recent log entries."""
