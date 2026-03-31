from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.api.dependencies import get_container
from app.core.container import ApplicationContainer

router = APIRouter(tags=["monitoring"])


@router.get("/posts")
def get_posts(limit: int = 60, container: ApplicationContainer = Depends(get_container)) -> dict[str, object]:
    return container.pipeline.list_posts(limit=limit)


@router.get("/scores")
def get_scores(container: ApplicationContainer = Depends(get_container)) -> dict[str, object]:
    return {
        "scores": [score.model_dump() for score in container.pipeline.list_scores()],
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/alerts")
def get_alerts(container: ApplicationContainer = Depends(get_container)) -> dict[str, object]:
    return {"alerts": [alert.model_dump() for alert in container.alerts.list_alerts()]}


@router.get("/logs")
def get_logs(limit: int = 100, container: ApplicationContainer = Depends(get_container)) -> dict[str, object]:
    return {"logs": [event.model_dump() for event in container.pipeline.list_logs(limit=limit)]}


@router.get("/bias")
def get_bias_summary(container: ApplicationContainer = Depends(get_container)) -> dict[str, object]:
    payload = container.pipeline.build_bias_summary()
    payload["as_of"] = datetime.now(timezone.utc).isoformat()
    return payload
