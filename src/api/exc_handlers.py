from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.apps import ApplicationError

__all__ = ('init_exception_handlers',)


async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, ApplicationError):
        message = exc.message
        status_code = exc.status_code
    else:
        message = str(exc)
        status_code = 500
    return JSONResponse(
        status_code=status_code,
        content={'message': message},
    )


def init_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        ApplicationError,
        exception_handler,
    )
