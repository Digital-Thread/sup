from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.apps import ApplicationException

__all__ = ('init_exception_handlers',)


exception_status_codes = {
    # ExampleNotFoundException: status.HTTP_404_NOT_FOUND,
    ApplicationException: status.HTTP_500_INTERNAL_SERVER_ERROR,
}


async def application_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    if isinstance(exc, ApplicationException):
        status_code = exception_status_codes.get(
            type(exc),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return JSONResponse(
        status_code=status_code,
        content={'message': str(exc)},
    )


def init_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        ApplicationException,
        application_error_handler,
    )
