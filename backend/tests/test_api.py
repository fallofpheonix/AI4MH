"""
Integration tests for the AI4MH FastAPI endpoints.

Uses httpx.TestClient (via starlette) to exercise the full API surface
including the alert lifecycle endpoints.
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi.testclient import TestClient

from main import app, _store

client = TestClient(app)


# ------------------------------------------------------------------ GET /api/posts


class TestGetPosts:
    def test_returns_list(self):
        resp = client.get("/api/posts")
        assert resp.status_code == 200
        data = resp.json()
        assert "posts" in data
        assert isinstance(data["posts"], list)
        assert "total" in data

    def test_limit_respected(self):
        resp = client.get("/api/posts?limit=3")
        assert resp.status_code == 200
        assert len(resp.json()["posts"]) <= 3


# ------------------------------------------------------------------ GET /api/scores


class TestGetScores:
    def test_returns_list(self):
        resp = client.get("/api/scores")
        assert resp.status_code == 200
        data = resp.json()
        assert "scores" in data
        assert isinstance(data["scores"], list)
        assert "updated_at" in data


# ------------------------------------------------------------------ GET /api/alerts


class TestGetAlerts:
    def test_returns_list(self):
        resp = client.get("/api/alerts")
        assert resp.status_code == 200
        data = resp.json()
        assert "alerts" in data
        assert isinstance(data["alerts"], list)


# ------------------------------------------------------------------ POST /api/ingest


class TestIngest:
    def test_ingest_returns_summary(self):
        resp = client.post("/api/ingest?n=5")
        assert resp.status_code == 200
        data = resp.json()
        assert "total_posts" in data
        assert "regions_scored" in data
        assert "alerts" in data
        assert data["total_posts"] >= 5


# ------------------------------------------------------------------ GET /api/logs


class TestGetLogs:
    def test_returns_list(self):
        resp = client.get("/api/logs")
        assert resp.status_code == 200
        data = resp.json()
        assert "logs" in data
        assert isinstance(data["logs"], list)

    def test_limit_respected(self):
        resp = client.get("/api/logs?limit=5")
        assert resp.status_code == 200
        assert len(resp.json()["logs"]) <= 5


# ------------------------------------------------------------------ GET /api/bias


class TestGetBias:
    def test_returns_structure(self):
        resp = client.get("/api/bias")
        assert resp.status_code == 200
        data = resp.json()
        assert "by_tier" in data
        assert "by_region" in data
        assert isinstance(data["by_tier"], dict)
        assert isinstance(data["by_region"], list)


# ------------------------------------------------------------------ alert lifecycle


class TestAlertLifecycle:
    def test_ack_alert(self, seeded_alert):
        alert_id = seeded_alert.id
        resp = client.post(f"/api/alerts/{alert_id}/ack")
        assert resp.status_code == 200
        assert resp.json()["alert"]["status"] == "acknowledged"

    def test_dismiss_alert(self, seeded_alert):
        alert_id = seeded_alert.id
        resp = client.post(f"/api/alerts/{alert_id}/dismiss")
        assert resp.status_code == 200
        assert resp.json()["alert"]["status"] == "dismissed"

    def test_resolve_alert(self, seeded_alert):
        alert_id = seeded_alert.id
        resp = client.post(f"/api/alerts/{alert_id}/resolve")
        assert resp.status_code == 200
        assert resp.json()["alert"]["status"] == "resolved"

    def test_unknown_alert_returns_404(self):
        resp = client.post("/api/alerts/nonexistent-id/ack")
        assert resp.status_code == 404

    def test_log_records_status_change(self, seeded_alert):
        alert_id = seeded_alert.id
        client.post(f"/api/alerts/{alert_id}/ack")
        resp = client.get("/api/logs?limit=50")
        events = [e["event"] for e in resp.json()["logs"]]
        assert "alert_status_changed" in events
