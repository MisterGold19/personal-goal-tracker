import logging  # standard logging system in python
import structlog  # for structural logs
import sys


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


setup_logging()

logger = structlog.get_logger()
