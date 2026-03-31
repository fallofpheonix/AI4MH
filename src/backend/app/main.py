from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.container import ApplicationContainer
from app.core.db import create_store
from app.services.alert_service import AlertService
from app.services.enrichment_service import EnrichmentService
from app.services.ingestion_service import IngestionService
from app.services.pipeline_service import PipelineService
from app.services.scoring_service import ScoringService


def build_container() -> ApplicationContainer:
    store = create_store()
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
    application.include_router(api_router, prefix=settings.api_prefix)
    return application


app = create_app()
