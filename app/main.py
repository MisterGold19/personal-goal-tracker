# run via uvicorn app.main:app --reload
# --reload - tryb developerski- nie musze ręcznie restartować serwer za każdym razem
from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from .core.config import settings
from .core.logging import logger
from pathlib import Path

# uvicorn potrzebuje instancji FastAPi
# uvicorn - to serwer
app = FastAPI()

placeholder_router = APIRouter(prefix="/api/v1")

# Podpięcie routera do aplikacji
app.include_router(placeholder_router)


@app.get("/")
def basic_get() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health")
def health() -> dict[str, str]:
    logger.info("health_check_started")
    return {"status": "ok", "app_version": settings.APP_VERSION}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = Path(__file__).parent / "static" / "favicon.ico"
    return FileResponse(favicon_path)
