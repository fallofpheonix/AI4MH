from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import get_container
from app.core.runtime import ApplicationContainer

router = APIRouter(tags=["ingestion"])


@router.post("/ingest")
def ingest(n: int = 30, container: ApplicationContainer = Depends(get_container)) -> dict[str, int]:
    return container.pipeline.run_cycle(n)
