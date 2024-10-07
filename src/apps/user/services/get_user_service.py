from typing import List

from src.apps.user.dtos import UserResponseDTO
from src.apps.user.exceptions import UserNotFoundError
from src.apps.user.repositories import IUserRepository


class GetUserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def get_user_by_email(self, email: str) -> UserResponseDTO:
        user = await self.repository.find_by_email(email)
        if user is None:
            raise UserNotFoundError('Пользователь не найден.')
        return user

    async def get_all_users(self) -> List[UserResponseDTO]:
        query = await self.repository.find_all_users()
        return query
