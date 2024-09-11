from fastapi import (
    FastAPI,
    Request,
)
from fastapi.responses import (
    JSONResponse,
)

from src.apps import (
    ApplicationError,
)

__all__ = ("init_exception_handlers",)


async def exception_handler(
    request: Request,
    exc: ApplicationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=ApplicationError.status_code,
        content={"message": exc.message},
    )


def init_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        ApplicationError,
        exception_handler,
    )
