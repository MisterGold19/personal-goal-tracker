from fastapi import APIRouter
from .schemas import HealthResponse
from app.core.config import settings
from app.core.logging import logger
from datetime import datetime, timezone


router = APIRouter(prefix="/api/v1")


def utc_now_z() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@router.get("/health", response_model=HealthResponse, summary="Health check endpoint")
def health() -> HealthResponse:
    logger.debug("health_debug_probe")
    return HealthResponse(
        status="ok", version=settings.APP_VERSION, time_utc=utc_now_z()
    )
