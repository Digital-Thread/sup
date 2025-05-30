from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.apps import ApplicationException
from src.apps.auth.exceptions import (
    InvalidTokenError,
    TokenExpireError,
    TokenRefreshExpireError,
)
from src.apps.comment import (
    CommentAssociatedWithBothError,
    CommentNotAssociatedError,
    CommentNotFoundError,
    CommentRepositoryError,
    FeatureOrTaskDoesNotExistsError,
    InvalidContentError,
)
from src.apps.feature.exceptions import (
    FeatureCreateError,
    FeatureDeleteError,
    FeatureDoesNotExistError,
    FeatureUpdateError,
)
from src.apps.project.exceptions import (
    ProjectException,
    ProjectNotFound,
    WorkspaceForProjectNotFound,
)
from src.apps.task.exceptions import (
    TaskCreateError,
    TaskDeleteError,
    TaskDoesNotExistError,
    TaskUpdateError,
)
from src.apps.user.exceptions import (
    InvalidEmailFormatError,
    InvalidNameError,
    InviteTokenExpiredError,
    LengthUserPasswordException,
    MissingDigitError,
    MissingSpecialCharacterError,
    MissingUppercaseLetterError,
    NotActivationExpire,
    OneOfTheExpire,
    PermissionDeniedException,
    TokenActivationExpire,
    TokenExpiredError,
    UserAlreadyExistsError,
    UserNotAdminError,
    UserNotFoundByEmailException,
    UserNotFoundError,
    UserPasswordException,
    UserPermissionError,
    ValidateEmptyLengthError,
    ValidateLengthError,
)

__all__ = ('init_exception_handlers',)

from src.apps.workspace.exceptions.category_exceptions import (
    CategoryException,
    CategoryNotDeleted,
    CategoryNotFound,
)
from src.apps.workspace.exceptions.role_exceptions import (
    RoleException,
    RoleNotDeleted,
    RoleNotFound,
)
from src.apps.workspace.exceptions.tag_exceptions import (
    TagException,
    TagNotDeleted,
    TagNotFound,
)
from src.apps.workspace.exceptions.workspace_exceptions import (
    MemberWorkspaceNotFound,
    WorkspaceAlreadyExists,
    WorkspaceException,
    WorkspaceNotFound,
)
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteNotFound,
    WorkspaceWorkspaceInviteNotFound,
)

exception_status_codes = {
    FeatureCreateError: status.HTTP_400_BAD_REQUEST,
    FeatureDeleteError: status.HTTP_400_BAD_REQUEST,
    FeatureDoesNotExistError: status.HTTP_404_NOT_FOUND,
    FeatureUpdateError: status.HTTP_400_BAD_REQUEST,
    TaskCreateError: status.HTTP_400_BAD_REQUEST,
    TaskDeleteError: status.HTTP_400_BAD_REQUEST,
    TaskDoesNotExistError: status.HTTP_404_NOT_FOUND,
    TaskUpdateError: status.HTTP_400_BAD_REQUEST,
    ApplicationException: status.HTTP_500_INTERNAL_SERVER_ERROR,
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
    InviteTokenExpiredError: status.HTTP_401_UNAUTHORIZED,
    NotActivationExpire: status.HTTP_401_UNAUTHORIZED,
    ValidateLengthError: status.HTTP_400_BAD_REQUEST,
    ValidateEmptyLengthError: status.HTTP_400_BAD_REQUEST,
    InvalidNameError: status.HTTP_400_BAD_REQUEST,
    InvalidEmailFormatError: status.HTTP_400_BAD_REQUEST,
    MissingUppercaseLetterError: status.HTTP_400_BAD_REQUEST,
    MissingDigitError: status.HTTP_400_BAD_REQUEST,
    MissingSpecialCharacterError: status.HTTP_400_BAD_REQUEST,
    OneOfTheExpire: status.HTTP_400_BAD_REQUEST,
    WorkspaceException: status.HTTP_400_BAD_REQUEST,
    WorkspaceAlreadyExists: status.HTTP_400_BAD_REQUEST,
    WorkspaceNotFound: status.HTTP_404_NOT_FOUND,
    MemberWorkspaceNotFound: status.HTTP_404_NOT_FOUND,
    CategoryException: status.HTTP_400_BAD_REQUEST,
    CategoryNotFound: status.HTTP_404_NOT_FOUND,
    CategoryNotDeleted: status.HTTP_400_BAD_REQUEST,
    RoleException: status.HTTP_400_BAD_REQUEST,
    RoleNotFound: status.HTTP_404_NOT_FOUND,
    RoleNotDeleted: status.HTTP_400_BAD_REQUEST,
    TagException: status.HTTP_400_BAD_REQUEST,
    TagNotFound: status.HTTP_404_NOT_FOUND,
    TagNotDeleted: status.HTTP_400_BAD_REQUEST,
    WorkspaceInviteNotFound: status.HTTP_404_NOT_FOUND,
    WorkspaceWorkspaceInviteNotFound: status.HTTP_404_NOT_FOUND,
    WorkspaceForProjectNotFound: status.HTTP_404_NOT_FOUND,
    ProjectException: status.HTTP_400_BAD_REQUEST,
    ProjectNotFound: status.HTTP_404_NOT_FOUND,
    InvalidContentError: status.HTTP_400_BAD_REQUEST,
    CommentNotAssociatedError: status.HTTP_400_BAD_REQUEST,
    CommentRepositoryError: status.HTTP_400_BAD_REQUEST,
    CommentAssociatedWithBothError: status.HTTP_400_BAD_REQUEST,
    FeatureOrTaskDoesNotExistsError: status.HTTP_400_BAD_REQUEST,
    CommentNotFoundError: status.HTTP_404_NOT_FOUND,
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
