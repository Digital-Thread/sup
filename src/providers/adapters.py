from typing import AsyncIterable

from dishka import Provider, Scope, provide
from environs import Env
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.apps.auth import JWTService
from src.apps.send_mail.service import SendMailService
from src.apps.user.protocols import JWTServiceProtocol, SendMailServiceProtocol
from src.apps.user.repositories import IUserRepository
from src.apps.user.services import (
    AuthenticateUserService,
    AuthorizeUserService,
    CreateUserService,
    GetUserService,
    UpdateUserService,
)
from src.apps.user.services.password_reset_user_service import PasswordResetUserService
from src.apps.user.services.remove_user_service import RemoveUserService
from src.config import Config, DbConfig, JWTConfig, RedisConfig, SMTPConfig
from src.data_access.reposotiries.user_repository import UserRepository


class SqlalchemyProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_engine(self, config: Config) -> AsyncEngine:
        return create_async_engine(config.db.construct_sqlalchemy_url)

    @provide(scope=Scope.APP)
    def provide_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(
        self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_config(self) -> Config:
        env = Env()
        env.read_env()

        return Config(
            db=DbConfig.from_env(env),
            smtp=SMTPConfig.from_env(env),
            redis=RedisConfig.from_env(env),
            jwt=JWTConfig.from_env(env),
        )

    @provide(scope=Scope.APP)
    def provide_smtp_config(self, config: Config) -> SMTPConfig:
        return config.smtp

    @provide(scope=Scope.APP)
    def provide_redis_config(self, config: Config) -> RedisConfig:
        return config.redis

    @provide(scope=Scope.APP)
    def provide_jwt_config(self, config: Config) -> JWTConfig:
        return config.jwt


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=scope, provides=SendMailServiceProtocol)
    def provide_send_mail_service(self, smtp_config: SMTPConfig) -> SendMailService:
        return SendMailService(smtp_config)

    @provide(scope=scope, provides=JWTServiceProtocol)
    def provide_jwt_protocol_service(
        self, jwt_config: JWTConfig, redis_config: RedisConfig
    ) -> JWTService:
        return JWTService(jwt_config, redis_config)

    @provide(scope=scope)
    def provide_jwt__service(self, jwt_config: JWTConfig, redis_config: RedisConfig) -> JWTService:
        return JWTService(jwt_config, redis_config)

    @provide(scope=scope, provides=IUserRepository)
    def provide_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @provide(scope=scope)
    def provide_pwd_context(self) -> CryptContext:
        return CryptContext(schemes=['bcrypt'], deprecated='auto')

    @provide(scope=scope)
    def provide_create_user_service(
        self,
        pwd_context: CryptContext,
        send_mail_service: SendMailServiceProtocol,
        repository: IUserRepository,
        redis_config: RedisConfig,
        token_service: JWTServiceProtocol,
    ) -> CreateUserService:
        return CreateUserService(
            pwd_context=pwd_context,
            send_mail_service=send_mail_service,
            repository=repository,
            redis_config=redis_config,
            token_service=token_service,
        )

    @provide(scope=scope)
    def provide_get_user_service(
        self, repository: IUserRepository, token_service: JWTServiceProtocol
    ) -> GetUserService:
        return GetUserService(repository=repository, token_service=token_service)

    @provide(scope=scope)
    def provide_authenticate_user_service(
        self,
        repository: IUserRepository,
        pwd_context: CryptContext,
        get_user_service: GetUserService,
    ) -> AuthenticateUserService:
        return AuthenticateUserService(
            repository=repository, pwd_context=pwd_context, get_user_service=get_user_service
        )

    @provide(scope=scope)
    def provide_authorize_user_service(
        self,
        repository: IUserRepository,
        token_service: JWTServiceProtocol,
    ) -> AuthorizeUserService:
        return AuthorizeUserService(repository=repository, token_service=token_service)

    @provide(scope=scope)
    def provide_update_user_service(
        self,
        repository: IUserRepository,
        token_service: JWTServiceProtocol,
    ) -> UpdateUserService:
        return UpdateUserService(repository=repository, token_service=token_service)

    @provide(scope=scope)
    def provide_remove_user_service(
        self,
        repository: IUserRepository,
    ) -> RemoveUserService:
        return RemoveUserService(repository=repository)

    @provide(scope=scope)
    def provide_reset_password_user_service(
        self,
        repository: IUserRepository,
        authenticate_service: AuthenticateUserService,
        create_service: CreateUserService,
    ) -> PasswordResetUserService:
        return PasswordResetUserService(
            repository=repository,
            authenticate_service=authenticate_service,
            create_service=create_service,
        )
