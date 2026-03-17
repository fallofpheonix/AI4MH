from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.alerts import router as alerts_router
from app.api.routes.ingest import router as ingest_router
from app.api.routes.monitoring import router as monitoring_router
from app.config import settings
from app.core.runtime import ApplicationContainer
from app.core.stores.sqlite import SQLiteStore
from app.services.alert_service import AlertService
from app.services.enrichment_service import EnrichmentService
from app.services.ingestion_service import IngestionService
from app.services.pipeline_service import PipelineService
from app.services.scoring_service import ScoringService


def build_container() -> ApplicationContainer:
    store = SQLiteStore(db_path=settings.sqlite_path, max_posts=settings.max_posts)
    ingestion = IngestionService()
    enrichment = EnrichmentService()
    scoring = ScoringService()
    alerts = AlertService(store)
    pipeline = PipelineService(
        store=store,
        ingestion=ingestion,
        enrichment=enrichment,
        scoring=scoring,
        alerts=alerts,
    )
    return ApplicationContainer(pipeline=pipeline, alerts=alerts)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.container = build_container()
    app.state.container.pipeline.bootstrap()
    yield


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name, lifespan=lifespan)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(monitoring_router, prefix=settings.api_prefix)
    application.include_router(ingest_router, prefix=settings.api_prefix)
    application.include_router(alerts_router, prefix=settings.api_prefix)
    return application


app = create_app()
