from __future__ import annotations

from dataclasses import dataclass

from app.services.alert_service import AlertService
from app.services.pipeline_service import PipelineService


@dataclass
class ApplicationContainer:
    pipeline: PipelineService
    alerts: AlertService
