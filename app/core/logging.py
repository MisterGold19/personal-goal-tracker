import logging  # standard logging system in python
import structlog  # for structural logs
from structlog.typing import Processor
from structlog.processors import CallsiteParameterAdder, CallsiteParameter
import sys
from .config import settings

_LVL_MAP = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def _to_numeric_level(name: str, default=logging.INFO) -> int:
    return _LVL_MAP.get((name or "").strip().upper(), default)


def setup_logging():
    num_lvl = _to_numeric_level(settings.LOG_LEVEL)

    logging.basicConfig(level=num_lvl, format="%(message)s", stream=sys.stdout)

    processors: list[Processor] = [
        structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
        structlog.processors.add_log_level,
        CallsiteParameterAdder(parameters={CallsiteParameter.MODULE}),
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
