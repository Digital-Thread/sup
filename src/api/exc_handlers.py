from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.apps import ApplicationError
from src.apps.auth.exceptions import (
    InvalidTokenError,
    TokenExpireError,
    TokenRefreshExpireError,
)
from src.apps.user.exceptions import (
    LengthUserPasswordException,
    PermissionDeniedException,
    TokenActivationExpire,
    TokenExpiredError,
    UserAlreadyExistsError,
    UserNotAdminError,
    UserNotFoundByEmailException,
    UserNotFoundError,
    UserPasswordException,
    UserPermissionError,
)

__all__ = ('init_exception_handlers',)

exception_status_codes = {
    ApplicationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    UserPasswordException: status.HTTP_401_UNAUTHORIZED,
    UserNotFoundError: status.HTTP_404_NOT_FOUND,
    UserAlreadyExistsError: status.HTTP_409_CONFLICT,
    TokenActivationExpire: status.HTTP_404_NOT_FOUND,
    UserNotFoundByEmailException: status.HTTP_404_NOT_FOUND,
    PermissionDeniedException: status.HTTP_403_FORBIDDEN,
    LengthUserPasswordException: status.HTTP_400_BAD_REQUEST,
    TokenExpiredError: status.HTTP_401_UNAUTHORIZED,
    InvalidTokenError: status.HTTP_400_BAD_REQUEST,
    TokenExpireError: status.HTTP_401_UNAUTHORIZED,
    TokenRefreshExpireError: status.HTTP_401_UNAUTHORIZED,
    UserPermissionError: status.HTTP_403_FORBIDDEN,
    UserNotAdminError: status.HTTP_403_FORBIDDEN,
}


async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, tuple(exception_status_codes.keys())):
        status_code = exception_status_codes[type(exc)]
        return JSONResponse(
            status_code=status_code,
            content={'message': str(exc)},
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'message': 'Internal Server Error'},
    )


def init_exception_handlers(app: FastAPI) -> None:
    for exc_class in exception_status_codes:
        app.add_exception_handler(exc_class, exception_handler)
    app.add_exception_handler(Exception, exception_handler)
