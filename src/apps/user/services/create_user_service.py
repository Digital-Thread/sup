import uuid
from datetime import timedelta

import redis.asyncio as redis  # type: ignore
from passlib.context import CryptContext

from src.apps.user.domain.entities import User
from src.apps.user.dtos import UserCreateDTO, UserResponseDTO
from src.apps.user.exceptions import (
    LengthUserPasswordException,
    TokenActivationExpire,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.apps.user.protocols import JWTServiceProtocol, SendMailServiceProtocol
from src.apps.user.repositories import IUserRepository
from src.apps.user.services import GetUserService
from src.config import RedisConfig


class CreateUserService:
    def __init__(
        self,
        pwd_context: CryptContext,
        send_mail_service: SendMailServiceProtocol,
        repository: IUserRepository,
        redis_config: RedisConfig,
        token_service: JWTServiceProtocol,
    ):
        self.repository = repository
        self.pwd_context = pwd_context or CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.send_mail_service = send_mail_service
        dsn = redis_config.construct_redis_dsn
        self.redis_client = redis.StrictRedis.from_url(dsn)
        self.token_service = token_service

    async def create_user(self, dto: UserCreateDTO) -> User:
        get_user_service = GetUserService(self.repository, self.token_service)
        existing_user = await get_user_service.get_user_by_email(dto.email)
        if existing_user:
            raise UserAlreadyExistsError(dto.email)
        user = User(**dto.model_dump())
        if len(user.password) > 51:
            raise LengthUserPasswordException
        user.password = self.get_password_hash(dto.password)
        await self.repository.save(user)
        activation_token = self.generate_activation_token(user.email)
        await self.redis_client.set(
            f'activation_token:{user.email}', activation_token, ex=timedelta(days=7)
        )
        await self.send_mail_service.send_activation_email(user.email, activation_token)
        return user

    async def activate_user(self, email: str) -> UserResponseDTO:
        user = await self.repository.find_by_email(email)
        if user is None:
            raise UserNotFoundError()
        user.is_active = True
        await self.repository.save(user)
        return user

    async def activate_user_by_token(self, email: str, token: str) -> UserResponseDTO:
        stored_token = await self.redis_client.get(f'activation_token:{email}')
        if stored_token is None or stored_token.decode() != token:
            raise TokenActivationExpire()
        user = await self.repository.find_by_email(email)
        if user is None:
            raise UserNotFoundError()
        user.is_active = True
        await self.repository.save(user)
        await self.redis_client.delete(f'activation_token:{email}')
        return user

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    @staticmethod
    def generate_activation_token(email: str) -> str:
        return str(uuid.uuid4())
