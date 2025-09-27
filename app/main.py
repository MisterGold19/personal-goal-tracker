# run via uvicorn app.main:app --reload
# --reload - tryb developerski- nie musze ręcznie restartować serwer za każdym razem
from fastapi import FastAPI, APIRouter
from .core.config import settings
from .core.logging import logger

# uvicorn potrzebuje instancji FastAPi
# uvicorn - to serwer
app = FastAPI()

placeholder_router = APIRouter(prefix="/api/v1")

# Podpięcie routera do aplikacji
app.include_router(placeholder_router)


@app.get("/health")
def health() -> dict[str, str]:
    logger.info("health_check_started")
    return {"status": "ok", "app_version": settings.APP_VERSION}
