from src.apps.user.exceptions import UserNotFoundByEmailException
from src.apps.user.repositories import IUserRepository


class RemoveUserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def remove_user(self, email: str) -> None:
        user = await self.repository.find_by_email(email)
        if not user:
            raise UserNotFoundByEmailException(email)
        return await self.repository.delete(user.email)
