from typing import AsyncIterable

from dishka import Provider, Scope, provide
from environs import Env
from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.apps.auth import JWTService
from src.apps.auth.repositories import IAuthRedisRepository, IPasswordRepository
from src.apps.auth.security.password_service import PasswordService
from src.apps.comment.domain import ICommentRepository
from src.apps.feature.repositories import IFeatureRepository
from src.apps.project.i_project_repository import IProjectRepository
from src.apps.user.protocols import JWTServiceProtocol, PasswordServiceProtocol
from src.apps.user.repositories import IUserRedisRepository, IUserRepository
from src.apps.user.services import (
    AuthenticateUserService,
    AuthorizeUserService,
    CreateUserService,
    GetUserService,
    UpdateUserService,
)
from src.apps.user.services.password_reset_user_service import PasswordResetUserService
from src.apps.user.services.remove_user_service import RemoveUserService
from src.apps.workspace.repositories import (
    ICategoryRepository,
    IRoleRepository,
    ITagRepository,
    IWorkspaceInviteRepository,
    IWorkspaceRepository,
)
from src.config import Config, DbConfig, JWTConfig, RedisConfig, SMTPConfig
from src.data_access.repositories import (
    CategoryRepository,
    CommentRepository,
    FeatureRepository,
    RoleRepository,
    TagRepository,
    WorkspaceInviteRepository,
    WorkspaceRepository,
)
from src.data_access.repositories.password_repository import PasswordRepository
from src.data_access.repositories.project_repository import ProjectRepository
from src.data_access.repositories.redis_repository import RedisRepository
from src.data_access.repositories.user_repository import UserRepository


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
            try:
                yield session
                await session.commit()
            except SQLAlchemyError:
                await session.rollback()
            finally:
                await session.close()


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

    feature_repository = provide(FeatureRepository, provides=IFeatureRepository)
    comment_repo = provide(CommentRepository, provides=ICommentRepository)
    workspace_repository = provide(WorkspaceRepository, provides=IWorkspaceRepository)
    workspace_invite_repository = provide(
        WorkspaceInviteRepository, provides=IWorkspaceInviteRepository
    )
    category_repository = provide(CategoryRepository, provides=ICategoryRepository)
    role_repository = provide(RoleRepository, provides=IRoleRepository)
    tag_repository = provide(TagRepository, provides=ITagRepository)
    project_repository = provide(ProjectRepository, provides=IProjectRepository)

    @provide(scope=scope, provides=JWTServiceProtocol)
    def provide_jwt_protocol_service(
            self, jwt_config: JWTConfig, redis_client: IAuthRedisRepository
    ) -> JWTService:
        return JWTService(jwt_config, redis_client=redis_client)

    @provide(scope=scope)
    def provide_pwd_context(self) -> CryptContext:
        return CryptContext(schemes=['bcrypt'], deprecated='auto')

    @provide(scope=scope, provides=IPasswordRepository)
    def provide_password_protocol_repository(self, pwd_context: CryptContext) -> PasswordRepository:
        return PasswordRepository(pwd_context=pwd_context)

    @provide(scope=scope, provides=PasswordServiceProtocol)
    def provide_password_protocol_service(self, repository: IPasswordRepository) -> PasswordService:
        return PasswordService(repository=repository)

    @provide(scope=scope)
    def provide_authenticate_user_service(
            self,
            repository: IUserRepository,
            password_service: PasswordServiceProtocol,
            get_user_service: GetUserService,
    ) -> AuthenticateUserService:
        return AuthenticateUserService(
            repository=repository,
            get_user_service=get_user_service,
            password_service=password_service,

        )

    @provide(scope=scope, provides=IAuthRedisRepository)
    def provide_auth_redis_repository(self, redis_config: RedisConfig) -> RedisRepository:
        return RedisRepository(redis_config=redis_config)

    @provide(scope=scope, provides=IUserRedisRepository)
    def provide_user_redis_repository(self, redis_config: RedisConfig) -> RedisRepository:
        return RedisRepository(redis_config=redis_config)

    @provide(scope=scope)
    def provide_jwt__service(
            self, jwt_config: JWTConfig, redis_client: IAuthRedisRepository
    ) -> JWTService:
        return JWTService(jwt_config, redis_client=redis_client)

    @provide(scope=scope, provides=IUserRepository)
    def provide_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @provide(scope=scope)
    def provide_create_user_service(
            self,
            repository: IUserRepository,
            redis_client: IUserRedisRepository,
            smtp_config: SMTPConfig,
            password_service: PasswordServiceProtocol,
    ) -> CreateUserService:
        return CreateUserService(
            repository=repository,
            redis_client=redis_client,
            password_service=password_service,
            smtp_config=smtp_config,
        )

    @provide(scope=scope)
    def provide_get_user_service(
            self, repository: IUserRepository, token_service: JWTServiceProtocol
    ) -> GetUserService:
        return GetUserService(repository=repository, token_service=token_service)

    @provide(scope=scope)
    def provide_authorize_user_service(
            self,
            repository: IUserRepository,
            get_user_service: GetUserService,
    ) -> AuthorizeUserService:
        return AuthorizeUserService(repository=repository, get_user_service=get_user_service)

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
