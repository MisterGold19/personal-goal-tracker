# run via uvicorn app.main:app --reload
# --reload - tryb developerski- nie musze ręcznie restartować serwer za każdym razem
from fastapi import FastAPI
from fastapi.responses import FileResponse
from .core.logging import RequestIdMiddleware
from pathlib import Path
from .metrics import setup_metrics_endpoint, setup_metrics_middleware
from .health.schemas import HealthResponse
from app.health.routes import router, health as routes_health


def create_app() -> FastAPI:
    # uvicorn potrzebuje instancji FastAPi
    # uvicorn - to serwer
    app = FastAPI(title="PGT")
    app.add_middleware(RequestIdMiddleware)  # podpięcie middleware
    setup_metrics_middleware(app)
    setup_metrics_endpoint(app)

    app.include_router(router)

    return app


app = create_app()


# def utc_now_z() -> str:
#     return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# @placeholder_router.get(
#     "/health", response_model=HealthResponse, summary="Health check endpoint"
# )
@app.get("/health", response_model=HealthResponse, summary="Health check endpoint")
def health() -> HealthResponse:
    return routes_health()


# def health() -> HealthResponse:
#     logger.debug("health_debug_probe")
#     return HealthResponse(
#         status="ok", version=settings.APP_VERSION, time_utc=utc_now_z()
#     )


@app.get("/")
def basic_get() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    favicon_path = Path(__file__).parent / "static" / "favicon.ico"
    return FileResponse(favicon_path)
