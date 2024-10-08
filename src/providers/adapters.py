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

from src.apps.meet import IMeetRepository, IParticipantRepository, MeetService
from src.apps.meet.protocols import WorkspaceService, WorkspaceServiceProtocol
from src.config import Config, DbConfig
from src.data_access.reposotiries.meet import MeetRepository
from src.data_access.reposotiries.meet_participant import ParticipantRepository


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
                raise
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
