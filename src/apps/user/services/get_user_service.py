from typing import List, Optional

from src.apps.user.domain.entity import User
from src.apps.user.exceptions import TokenExpiredError, UserNotFoundError
from src.apps.user.protocols import JWTServiceProtocol
from src.apps.user.repository import IUserRepository


class GetUserService:
    def __init__(self, repository: IUserRepository, token_service: JWTServiceProtocol):
        self.repository = repository
        self.token_service = token_service

    async def get_user_by_email(self, email: str) -> User:
        user = await self.repository.find_by_email(email)
        if user:
            return user
        else:
            raise UserNotFoundError()

    async def get_all_users(
        self, limit: int, offset: int, sort_by: Optional[str] = None, sort_order: str = 'asc'
    ) -> List[User]:
        users = await self.repository.find_all_users(limit, offset, sort_by, sort_order)
        return users

    async def get_user_info(
        self, access_token: str, refresh_token: str, user_agent: str
    ) -> tuple[User, Optional[str], Optional[int], Optional[str], Optional[int]]:

        user: Optional[User] = None
        new_access_token = None
        max_age_access = None
        new_refresh_token = None
        max_age_refresh = None

        if access_token:
            email = await self.token_service.decode_access_token(access_token)
            is_valid = await self.token_service.access_token_protected_resource(
                email=email, access_token_client=access_token, user_agent=user_agent
            )
            if is_valid:
                user = await self.get_user_by_email(email)
                return (
                    user,
                    new_access_token,
                    max_age_access,
                    new_refresh_token,
                    max_age_refresh,
                )

        if refresh_token:
            email = await self.token_service.decode_refresh_token(refresh_token)
            is_valid = await self.token_service.refresh_token_protected_resource(
                email=email, refresh_token_client=refresh_token, user_agent=user_agent
            )
            if is_valid:
                new_access_token, max_age_access, new_refresh_token, max_age_refresh = (
                    await self.token_service.creating_tokens(email=email, user_agent=user_agent)
                )
                user = await self.get_user_by_email(email)
                return (
                    user,
                    new_access_token,
                    max_age_access,
                    new_refresh_token,
                    max_age_refresh,
                )
        if user is None:
            raise TokenExpiredError()
        return (
            user,
            new_access_token,
            max_age_access,
            new_refresh_token,
            max_age_refresh,
        )
