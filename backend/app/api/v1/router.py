from fastapi import APIRouter

from app.api.v1.routes.alerts import router as alerts_router
from app.api.v1.routes.ingest import router as ingest_router
from app.api.v1.routes.monitoring import router as monitoring_router

router = APIRouter()
router.include_router(monitoring_router)
router.include_router(ingest_router)
router.include_router(alerts_router)
