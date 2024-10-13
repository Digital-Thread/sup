from typing import List, Optional

from src.apps.auth.exceptions import TokenExpireError
from src.apps.user.dtos import UserResponseDTO
from src.apps.user.protocols import JWTServiceProtocol
from src.apps.user.repositories import IUserRepository


class GetUserService:
    def __init__(self, repository: IUserRepository, token_service: JWTServiceProtocol):
        self.repository = repository
        self.token_service = token_service

    async def get_user_by_email(self, email: str) -> UserResponseDTO:
        user = await self.repository.find_by_email(email)
        return user

    async def get_all_users(self) -> List[UserResponseDTO]:
        query = await self.repository.find_all_users()
        return query

    async def get_user_info(
        self, access_token: str, refresh_token: str, user_agent: str
    ) -> tuple[UserResponseDTO, str, int, str, int]:

        user = None
        new_access_token = None
        max_age_access = None
        new_refresh_token = None
        max_age_refresh = None

        if access_token:
            try:
                decoded_payload = await self.token_service.decode_token(access_token)
                email = decoded_payload['email']
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
            except TokenExpireError:
                pass

        if refresh_token:
            decoded_payload = await self.token_service.decode_token(refresh_token)
            email = decoded_payload['email']
            is_valid = await self.token_service.refresh_token_protected_resource(
                email=email, refresh_token_client=refresh_token, user_agent=user_agent
            )
            if is_valid:
                new_access_token, max_age_access, new_refresh_token, max_age_refresh = (
                    await self.token_service.creating_tokens(email=email, user_agent=user_agent)
                )
                user = await self.get_user_by_email(email)
                if user:
                    return (
                        user,
                        new_access_token,
                        max_age_access,
                        new_refresh_token,
                        max_age_refresh,
                    )
                else:
                    raise TokenExpireError()

        return user, new_access_token, max_age_access, new_refresh_token, max_age_refresh
