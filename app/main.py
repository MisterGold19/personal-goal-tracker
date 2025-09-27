# run via uvicorn app.main:app --reload
# --reload - tryb developerski- nie musze ręcznie restartować serwer za każdym razem
from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from .core.config import settings
from .core.logging import logger, RequestIdMiddleware
from pathlib import Path
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Literal

# uvicorn potrzebuje instancji FastAPi
# uvicorn - to serwer
app = FastAPI()
app.add_middleware(RequestIdMiddleware)  # podpięcie middleware

placeholder_router = APIRouter(prefix="/api/v1")


class HealthResponse(BaseModel):
    status: Literal["ok"] = Field("ok")
    version: str = Field("v0.1.0")
    time_utc: str = Field("2025-09-27T19:44:35Z")


def utc_now_z() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@placeholder_router.get(
    "/health", response_model=HealthResponse, summary="Health check endpoint"
)
def health() -> HealthResponse:
    logger.debug("health_debug_probe")
    return HealthResponse(
        status="ok", version=settings.APP_VERSION, time_utc=utc_now_z()
    )


# Podpięcie routera do aplikacji
app.include_router(placeholder_router)


@app.get("/")
def basic_get() -> dict[str, str]:
    return {"status": "ok"}


# @app.get("/health")
# def health() -> dict[str, str]:
#     return {"status": "ok", "app_version": settings.APP_VERSION}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    favicon_path = Path(__file__).parent / "static" / "favicon.ico"
    return FileResponse(favicon_path)
