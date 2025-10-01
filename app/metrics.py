from fastapi import FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, generate_latest, Counter
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable

HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",  # metric name (must be unique)
    "Total number of HTTP requests",  # description
    ["method", "path", "status"],  # lables
)


class HttpRequestCounterMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        method = request.method
        route = request.scope.get("route")
        templated_path = getattr(route, "path", None) or request.url.path

        try:
            response = await call_next(request)
            status = str(response.status_code)
            return response
        except Exception:
            status = "500"
            raise
        finally:
            HTTP_REQUESTS_TOTAL.labels(
                method=method, path=templated_path, status=status
            ).inc()


def setup_metrics_endpoint(app: FastAPI) -> None:
    # nie importuje app do metrics -
    # brak cyklicznych importów -
    # moduł nie zna szczegółow aplikacji
    @app.get("/metrics")
    # metryki sa poza prefiksem apirouter
    async def metrics() -> Response:
        # print(f"{REGISTRY}")
        data = generate_latest(REGISTRY)
        # print(f"{data}", "\n", f"{CONTENT_TYPE_LATEST}")
        return Response(content=data, media_type=CONTENT_TYPE_LATEST)


def setup_metrics_middleware(app: FastAPI) -> None:
    app.add_middleware(HttpRequestCounterMiddleware)
