from typing import AsyncIterable

from dishka import Provider, Scope, provide
from environs import Env
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.apps.comment.domain import ICommentRepository
from src.config import Config, DbConfig
from src.apps.workspace.repositories import (
    ICategoryRepository,
    IRoleRepository,
    ITagRepository,
    IWorkspaceInviteRepository,
    IWorkspaceRepository,
)
from src.apps.comment.domain import (
    CommentEntity,
    CommentId,
    Content,
    ICommentRepository,
)
from src.data_access.reposotiries import (
    CategoryRepository,
    RoleRepository,
    TagRepository,
    WorkspaceInviteRepository,
    WorkspaceRepository,
)
from src.data_access.reposotiries import CommentRepository
from src.apps.project.i_project_repository import IProjectRepository
from src.config import Config, DbConfig
from src.data_access.reposotiries.project_repository import ProjectRepository


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
        )


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST
    
    comment_repo = provide(CommentRepository, provides=ICommentRepository)
    workspace_repository = provide(WorkspaceRepository, provides=IWorkspaceRepository)
    workspace_invite_repository = provide(
        WorkspaceInviteRepository, provides=IWorkspaceInviteRepository
    )
    category_repository = provide(CategoryRepository, provides=ICategoryRepository)
    role_repository = provide(RoleRepository, provides=IRoleRepository)
    tag_repository = provide(TagRepository, provides=ITagRepository)
    comment_repo = provide(
        CommentRepository, provides=ICommentRepository[Content, CommentId, CommentEntity]
    )
    project_repository = provide(ProjectRepository, provides=IProjectRepository)
