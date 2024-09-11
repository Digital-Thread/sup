import structlog
from structlog.processors import (
    CallsiteParameter,
    CallsiteParameterAdder,
)

from .configuration import (
    _configure_default_logging_by_custom,
)


def configure_logging(enable_json_logs: bool = False) -> None:
    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")

    shared_processors = [
        timestamper,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.contextvars.merge_contextvars,
        CallsiteParameterAdder(
            {
                CallsiteParameter.PATHNAME,
                CallsiteParameter.FILENAME,
                CallsiteParameter.MODULE,
                CallsiteParameter.FUNC_NAME,
                CallsiteParameter.THREAD,
                CallsiteParameter.THREAD_NAME,
                CallsiteParameter.PROCESS,
                CallsiteParameter.PROCESS_NAME,
            }
        ),
        structlog.stdlib.ExtraAdder(),
    ]

    structlog.configure(
        processors=shared_processors
        + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        # call log with await syntax in thread pool executor
        wrapper_class=structlog.stdlib.AsyncBoundLogger,
        cache_logger_on_first_use=True,
    )

    logs_render = (
        structlog.processors.JSONRenderer()
        if enable_json_logs
        else structlog.dev.ConsoleRenderer(colors=True)
    )
    _configure_default_logging_by_custom(shared_processors, logs_render)
