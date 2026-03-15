"""
Pytest configuration for the AI4MH backend test suite.

Provides shared fixtures used across test modules.
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from models.alert import Alert


@pytest.fixture()
def seeded_alert():
    """
    Inject a deterministic *review_required* alert into the store so that
    alert-lifecycle tests can run without relying on probabilistic ingestion.

    The alert is removed after the test completes.
    """
    from main import _store

    alert = Alert(
        id="test-alert-fixture",
        region="CA-LA",
        score=0.90,
        status="review_required",
        confidence=0.80,
        sample_size=25,
        score_breakdown={},
        evidence_post_ids=[],
    )
    existing = _store.get_alerts()
    _store.save_alerts(existing + [alert])

    yield alert

    # Restore the original alert list (remove the fixture alert).
    alerts = _store.get_alerts()
    _store.save_alerts([a for a in alerts if a.id != "test-alert-fixture"])
