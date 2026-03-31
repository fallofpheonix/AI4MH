from __future__ import annotations


def test_ingest_returns_operational_summary(client):
    response = client.post("/api/v1/ingest?n=12")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_posts"] >= 12
    assert payload["regions_scored"] >= 1


def test_monitoring_endpoints_return_expected_shapes(client):
    client.post("/api/v1/ingest?n=12")

    posts = client.get("/api/v1/posts?limit=5")
    scores = client.get("/api/v1/scores")
    alerts = client.get("/api/v1/alerts")
    logs = client.get("/api/v1/logs?limit=10")
    bias = client.get("/api/v1/bias")

    assert posts.status_code == 200
    assert isinstance(posts.json()["posts"], list)
    assert isinstance(scores.json()["scores"], list)
    assert isinstance(alerts.json()["alerts"], list)
    assert isinstance(logs.json()["logs"], list)
    assert "by_tier" in bias.json()


def test_alert_lifecycle_writes_log_entry(client, seeded_alert):
    response = client.post(f"/api/v1/alerts/{seeded_alert.id}/ack")

    assert response.status_code == 200
    assert response.json()["alert"]["status"] == "acknowledged"

    logs = client.get("/api/v1/logs?limit=20").json()["logs"]
    assert any(entry["event"] == "alert_status_changed" for entry in logs)


def test_unknown_alert_returns_404(client):
    response = client.post("/api/v1/alerts/missing-alert/resolve")
    assert response.status_code == 404
