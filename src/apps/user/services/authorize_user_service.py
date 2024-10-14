from typing import List

from src.apps.user.domain.entities import User
from src.apps.user.dtos import UserResponseDTO
from src.apps.user.exceptions import (
    UserNotAdminError,
    UserNotFoundError,
    UserPermissionError,
)
from src.apps.user.protocols import JWTServiceProtocol
from src.apps.user.repositories import IUserRepository
from src.apps.user.services import GetUserService


class AuthorizeUserService:

    def __init__(
        self,
        repository: IUserRepository,
        token_service: JWTServiceProtocol,
    ):
        self.repository = repository
        self.token_service = token_service

    async def get_authorize_user_by_email(self, user: User, email: str) -> UserResponseDTO:
        get_user_service = GetUserService(self.repository, self.token_service)
        if user is None:
            raise UserNotFoundError()
        if not user.is_superuser and user.email != email:
            raise UserNotAdminError()
        if user.is_superuser and user.is_active:
            return await get_user_service.get_user_by_email(email)
        if not user.is_superuser and user.email == email:
            return await get_user_service.get_user_by_email(email)
        else:
            raise UserPermissionError()

    async def get_authorize_users(self, user: User) -> List[UserResponseDTO]:
        get_user_service = GetUserService(self.repository, self.token_service)
        if user.is_superuser and user.is_active:
            return await get_user_service.get_all_users()
        else:
            raise UserPermissionError()
