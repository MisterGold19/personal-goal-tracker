# run via uvicorn app.main:app --reload
# --reload - tryb developerski- nie musze ręcznie restartować serwer za każdym razem
from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from .core.config import settings
from .core.logging import logger, RequestIdMiddleware
from pathlib import Path

# uvicorn potrzebuje instancji FastAPi
# uvicorn - to serwer
app = FastAPI()
app.add_middleware(RequestIdMiddleware)  # podpięcie middleware

placeholder_router = APIRouter(prefix="/api/v1")


@placeholder_router.get("/health")
def health() -> dict[str, str]:
    logger.debug("health_debug_probe")
    return {"status": "ok", "app_version": settings.APP_VERSION}


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
