from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import get_container
from app.core.container import ApplicationContainer

router = APIRouter(tags=["alerts"])


@router.post("/alerts/{alert_id}/ack")
def acknowledge_alert(alert_id: str, container: ApplicationContainer = Depends(get_container)) -> dict[str, object]:
    return {"alert": container.alerts.transition(alert_id, "acknowledged").model_dump()}


@router.post("/alerts/{alert_id}/dismiss")
def dismiss_alert(alert_id: str, container: ApplicationContainer = Depends(get_container)) -> dict[str, object]:
    return {"alert": container.alerts.transition(alert_id, "dismissed").model_dump()}


@router.post("/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: str, container: ApplicationContainer = Depends(get_container)) -> dict[str, object]:
    return {"alert": container.alerts.transition(alert_id, "resolved").model_dump()}
