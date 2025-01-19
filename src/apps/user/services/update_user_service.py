from src.apps.user.domain.entity import User
from src.apps.user.dtos import UserUpdateDTO
from src.apps.user.exceptions import UserAlreadyExistsError
from src.apps.user.protocols import JWTServiceProtocol
from src.apps.user.repositories import IUserRepository


class UpdateUserService:
    def __init__(self, repository: IUserRepository, token_service: JWTServiceProtocol):
        self.repository = repository
        self.token_service = token_service

    async def update_user(self, user: User, user_data: UserUpdateDTO, user_agent: str) -> User:
        if user_data.email and user_data.email != user.email:
            existing_user = await self.repository.find_by_email(user_data.email)
            if existing_user:
                raise UserAlreadyExistsError(user_data.email)
            user_data.email = user_data.email.lower()
            await self.token_service.removing_tokens(email=user_data.email, user_agent=user_agent)
            await self.token_service.creating_tokens(email=user_data.email, user_agent=user_agent)
        for key, value in user_data.__dict__.items():
            if value:
                if key == 'first_name' and value:
                    user_data.first_name = value.capitalize()
                if key == 'last_name' and value:
                    user_data.last_name = value.capitalize()
                if key == 'email' and value:
                    user_data.email = value.lower()

                setattr(user, key, getattr(user_data, key))
                if key in ['first_name', 'last_name', 'email', 'username_tg', 'nick_tg', 'nick_gmeet']:
                    user.validate_length(value, key)
                    if key in ['first_name', 'last_name']:
                        user.validate_name(value)
                    if key == 'email':
                        user.validate_email(value)
                elif key in ['nick_gitlab', 'nick_github']:
                    user.validate_length(value, key)

        await self.repository.update(user)
        return user
