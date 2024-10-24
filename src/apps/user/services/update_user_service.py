from src.apps.user.domain.entities import User
from src.apps.user.dtos import UserUpdateDTO
from src.apps.user.exceptions import UserAlreadyExistsError
from src.apps.user.protocols import JWTServiceProtocol
from src.apps.user.repositories import IUserRepository


class UpdateUserService:
    def __init__(self, repository: IUserRepository, token_service: JWTServiceProtocol):
        self.repository = repository
        self.token_service = token_service

    async def update_user(self, user: User, user_data: UserUpdateDTO, user_agent: str) -> User:
        if user_data.email:
            existing_user = await self.repository.find_by_email(user_data.email)
            if existing_user:
                raise UserAlreadyExistsError(user_data.email)
            await self.token_service.removing_tokens(email=user_data.email, user_agent=user_agent)
            await self.token_service.creating_tokens(email=user_data.email, user_agent=user_agent)
        for key, value in user_data.__dict__.items():
            if value:
                setattr(user, key, value)
        await self.repository.update(user)
        return user
