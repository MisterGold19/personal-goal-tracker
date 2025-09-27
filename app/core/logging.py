import logging  # standard logging system in python
import structlog  # for structural logs
import sys
from structlog.typing import Processor, EventDict, WrappedLogger
from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time
from typing import Optional, Callable, Awaitable
from types import FrameType


from .config import settings

_LVL_MAP = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def _to_numeric_level(name: str, default: int = logging.INFO) -> int:
    return _LVL_MAP.get((name or "").strip().upper(), default)


def add_version(
    logger: WrappedLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    event_dict.setdefault("version", settings.APP_VERSION)
    return event_dict


def add_module(
    logger: WrappedLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    if "module" in event_dict and event_dict["module"]:
        return event_dict
    ignore_prefixes = ("structlog", "logging", "uvicorn", "fastapi", "starlette")
    preferred_prefix = "app."

    frame: Optional[FrameType] = sys._getframe()
    candidate = None
    while frame:
        mod = frame.f_globals.get("__name__", "")
        if mod and not mod.startswith(ignore_prefixes):
            if candidate is None:
                candidate = mod
            if mod.startswith(preferred_prefix):
                candidate = mod
                break
        frame = frame.f_back

    event_dict["module"] = candidate or event_dict.get("module") or "unknown"
    return event_dict


def setup_logging() -> None:
    num_lvl = _to_numeric_level(settings.LOG_LEVEL)

    logging.basicConfig(level=num_lvl, format="%(message)s", stream=sys.stdout)

    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logging.getLogger(name).setLevel(num_lvl)

    processors: list[Processor] = [
        structlog.processors.TimeStamper(fmt="iso", utc=False, key="timestamp"),
        add_version,
        structlog.processors.add_log_level,
        structlog.contextvars.merge_contextvars,
        # CallsiteParameterAdder(
        #     parameters={CallsiteParameter.MODULE},
        #     additional_ignores=[
        #         "structlog",
        #         "logging",
        #         "uvicorn",
        #         "fastapi",
        #         "app.core.logging",
        #     ],
        # ),
        add_module,
        structlog.processors.JSONRenderer(),  # must be always last one in processors
    ]

    structlog.configure(
        processors=processors,
        context_class=dict,
        wrapper_class=structlog.make_filtering_bound_logger(num_lvl),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


setup_logging()

logger = structlog.get_logger()


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        rid = request.headers.get("X-Request-ID") or str(uuid4())
        structlog.contextvars.bind_contextvars(request_id=rid)

        start = time.perf_counter()
        status_code = None
        response: Response | None = None
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        except Exception:
            status_code = 500
            raise
        finally:
            endpoint = request.scope.get("endpoint")
            handler_module = getattr(endpoint, "__module__", None) if endpoint else None
            if handler_module:
                structlog.contextvars.bind_contextvars(module=handler_module)
            duration_ms = (time.perf_counter() - start) * 1000.0
            logger.info(
                "request_completed",
                duration_ms=round(duration_ms, 2),
                status_code=status_code,
                method=request.method,
                path=request.url.path,
            )
            structlog.contextvars.clear_contextvars()
