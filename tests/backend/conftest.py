from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.core.container import ApplicationContainer
from app.crud.memory import MemoryStore
from app.main import create_app
from app.schemas.alert import Alert
from app.services.alert_service import AlertService
from app.services.enrichment_service import EnrichmentService
from app.services.ingestion_service import IngestionService
from app.services.pipeline_service import PipelineService
from app.services.scoring_service import ScoringService


@pytest.fixture()
def store() -> MemoryStore:
    return MemoryStore(max_posts=250)


@pytest.fixture()
def client(store: MemoryStore):
    alerts = AlertService(store)
    container = ApplicationContainer(
        pipeline=PipelineService(
            store=store,
            ingestion=IngestionService(),
            enrichment=EnrichmentService(),
            scoring=ScoringService(),
            alerts=alerts,
        ),
        alerts=alerts,
    )

    with patch("app.main.build_container", return_value=container):
        app = create_app()
        with TestClient(app) as test_client:
            yield test_client


@pytest.fixture()
def seeded_alert(store: MemoryStore) -> Alert:
    alert = Alert(
        id="test-alert-fixture",
        region="CA-LA",
        score=0.90,
        status="review_required",
        confidence=0.80,
        sample_size=25,
    )
    store.save_alerts([alert])
    return alert
