import logging
from typing import Any, Callable

import structlog
from structlog.types import EventDict, WrappedLogger


def _extract_from_record(_: WrappedLogger, __: str, event_dict: EventDict) -> EventDict:
    # Extract thread and process names and add them to the event dict.
    record = event_dict['_record']
    event_dict['thread_name'] = record.threadName
    event_dict['process_name'] = record.processName
    return event_dict


def _configure_default_logging_by_custom(
    shared_processors: list[Callable[..., Any]],
    logs_render: Any,
) -> None:
    handler = logging.StreamHandler()

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            _extract_from_record,
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            logs_render,
        ],
    )

    handler.setFormatter(formatter)
    root_uvicorn_logger = logging.getLogger()
    root_uvicorn_logger.addHandler(handler)
    root_uvicorn_logger.setLevel(logging.INFO)
