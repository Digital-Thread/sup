from typing import AsyncIterable

from dishka import Provider, Scope, from_context, provide
from environs import Env
from fastapi import Request
from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.apps.auth import JWTService
from src.apps.comment import ICommentRepository
from src.apps.feature import IFeatureRepository
from src.apps.meet import IMeetRepository, IParticipantRepository, MeetService
from src.apps.meet.protocols import WorkspaceService, WorkspaceServiceProtocol
from src.apps.permission import IPermissionGroupRepository, IPermissionRepository
from src.apps.project.project_repository import IProjectRepository
from src.apps.send_mail.service import SendMailService
from src.apps.task import ITaskRepository
from src.apps.user.protocols import JWTServiceProtocol, SendMailServiceProtocol
from src.apps.user.repository import IUserRepository
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
from src.apps.workspace.repositories.user_workspace_role_repository import (
    IUserWorkspaceRoleRepository,
)
from src.config import Config, DbConfig, JWTConfig, RedisConfig, SMTPConfig
from src.data_access.repositories import (
    CategoryRepository,
    CommentRepository,
    FeatureRepository,
    PermissionGroupRepository,
    PermissionRepository,
    RoleRepository,
    TagRepository,
    TaskRepository,
    WorkspaceInviteRepository,
    WorkspaceRepository,
)
from src.data_access.repositories.meet import MeetRepository
from src.data_access.repositories.meet_participant import ParticipantRepository
from src.data_access.repositories.project_repository import ProjectRepository
from src.data_access.repositories.user_repository import UserRepository
from src.data_access.repositories.user_workspace_role_repository import (
    UserWorkspaceRoleRepository,
)
from src.providers.context import WorkspaceContext


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


class WorkspaceProvider(Provider):
    scope = Scope.REQUEST
    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide
    def provide_workspace_context(self, request: Request) -> WorkspaceContext:
        workspace_id = getattr(request.state, 'workspace_id', None)
        return WorkspaceContext(workspace_id=workspace_id)


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    feature_repository = provide(FeatureRepository, provides=IFeatureRepository)
    task_repository = provide(TaskRepository, provides=ITaskRepository)
    comment_repo = provide(CommentRepository, provides=ICommentRepository)
    workspace_repository = provide(WorkspaceRepository, provides=IWorkspaceRepository)
    workspace_invite_repository = provide(
        WorkspaceInviteRepository, provides=IWorkspaceInviteRepository
    )
    category_repository = provide(CategoryRepository, provides=ICategoryRepository)
    role_repository = provide(RoleRepository, provides=IRoleRepository)
    user_workspace_role_repository = provide(
        UserWorkspaceRoleRepository, provides=IUserWorkspaceRoleRepository
    )
    tag_repository = provide(TagRepository, provides=ITagRepository)
    project_repository = provide(ProjectRepository, provides=IProjectRepository)
    permission_repository = provide(PermissionRepository, provides=IPermissionRepository)
    permission_group_repository = provide(
        PermissionGroupRepository, provides=IPermissionGroupRepository
    )

    @provide(scope=scope, provides=SendMailServiceProtocol)
    def provide_send_mail_service(self) -> SendMailService:
        return SendMailService()

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
        smtp_config: SMTPConfig,
    ) -> CreateUserService:
        return CreateUserService(
            pwd_context=pwd_context,
            send_mail_service=send_mail_service,
            repository=repository,
            redis_config=redis_config,
            smtp_config=smtp_config,
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

    @provide(scope=scope)
    def provide_meet_repository(self, session: AsyncSession) -> IMeetRepository:
        return MeetRepository(session)

    @provide(scope=scope)
    def provide_participant_repository(self, session: AsyncSession) -> IParticipantRepository:
        return ParticipantRepository(session)

    @provide(scope=scope)
    def provide_temp_workspace_service(self) -> WorkspaceServiceProtocol:
        return WorkspaceService()

    @provide(scope=scope)
    def provide_meet_service(
        self,
        meet_repository: IMeetRepository,
        participant_repository: IParticipantRepository,
        workspace_service: WorkspaceServiceProtocol,
    ) -> MeetService:
        return MeetService(
            meet_repository=meet_repository,
            participant_repository=participant_repository,
            workspace_service=workspace_service,
        )
