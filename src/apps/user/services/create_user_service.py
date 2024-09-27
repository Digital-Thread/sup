from passlib.context import CryptContext

from src.apps.user.domain.entities import User
from src.apps.user.dtos import UserCreateDTO, UserResponseDTO
from src.apps.user.exceptions import UserAlreadyExistsError, UserNotFoundError
from src.apps.user.services import GetUserService, UserService


class CreateUserService(UserService):
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def create_user(self, dto: UserCreateDTO) -> UserResponseDTO:
        get_user_service = GetUserService(self.repository)
        existing_user = get_user_service.get_user_by_email(dto.email)
        if existing_user:
            raise UserAlreadyExistsError(dto.email)
        user = User(**dto.model_dump())
        user.password = self.get_password_hash(dto.password)
        self.repository.save(user)
        return user

    def activate_user(self, email: str) -> UserResponseDTO:
        user = self.repository.find_by_email(email)
        if user is None:
            raise UserNotFoundError('Пользователь не найден.')
        user.is_active = True
        self.repository.save(user)
        return user

    def get_password_hash(self, password: str) -> str:
        """Получение хеш-пароля"""
        return self.pwd_context.hash(password)
