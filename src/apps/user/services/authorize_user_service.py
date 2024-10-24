from typing import List

from src.apps.user.domain.entities import User
from src.apps.user.exceptions import (
    UserNotAdminError,
    UserNotFoundError,
    UserPermissionError,
)
from src.apps.user.repositories import IUserRepository
from src.apps.user.services import GetUserService


class AuthorizeUserService:

    def __init__(
        self,
        repository: IUserRepository,
        get_user_service: GetUserService,
    ):
        self.repository = repository
        self.get_user_service = get_user_service

    @staticmethod
    async def get_access_admin(user: User) -> bool:
        if user is None:
            raise UserNotFoundError()
        if user.is_superuser:
            return True
        else:
            raise UserPermissionError()

    async def get_authorize_user_by_email(self, user: User, email: str) -> User:
        if user is None:
            raise UserNotFoundError()
        if not user.is_superuser and user.email != email:
            raise UserNotAdminError()
        if user.is_superuser and user.is_active:
            user = await self.get_user_service.get_user_by_email(email)
            return user
        if not user.is_superuser and user.email == email:
            user = await self.get_user_service.get_user_by_email(email)
            return user
        else:
            raise UserPermissionError()

    @staticmethod
    async def get_authorize_users(user: User) -> bool:
        if user.is_superuser and user.is_active:
            return True
        else:
            raise UserPermissionError()
