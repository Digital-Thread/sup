from logging import warning

from asyncpg.exceptions import ForeignKeyViolationError
from sqlalchemy import delete, exists, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.workspace.domain.entities.workspace import WorkspaceEntity
from src.apps.workspace.domain.types_ids import MemberId, OwnerId, WorkspaceId
from src.apps.workspace.exceptions.workspace_exceptions import (
    MemberWorkspaceNotFound,
    WorkspaceAlreadyExists,
    WorkspaceNotFound,
    WorkspaceNotUpdated,
)
from src.apps.workspace.repositories.workspace_repository import IWorkspaceRepository
from src.data_access.converters.workspace_converter import WorkspaceConverter
from src.data_access.models import (
    WorkspaceMemberModel,
    WorkspaceModel,
)


class WorkspaceRepository(IWorkspaceRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def save(self, workspace: WorkspaceEntity) -> None:
        stmt = WorkspaceConverter.entity_to_model(workspace)
        self._session.add(stmt)
        try:
            await self._session.flush()
            workspace._id = WorkspaceId(stmt.id)
        except IntegrityError as error:
            warning(error)
            if isinstance(error.orig.__cause__, ForeignKeyViolationError):
                raise MemberWorkspaceNotFound(f'Владелец с id={workspace.owner_id} не существует')
            raise WorkspaceAlreadyExists(
                f'Рабочее пространство с именем {workspace.name} уже существует'
            )

    async def find_by_id(self, workspace_id: WorkspaceId) -> WorkspaceEntity | None:
        query = select(WorkspaceModel).filter_by(id=workspace_id)
        result = await self._session.execute(query)
        try:
            workspace_model = result.scalar_one()
        except NoResultFound as error:
            warning(error)
            raise WorkspaceNotFound(f'Рабочее пространство с id={workspace_id} не найдено')
        else:
            workspace_entity = WorkspaceConverter.model_to_entity(workspace_model)
            return workspace_entity

    async def find_by_member_id(self, member_id: MemberId) -> list[WorkspaceEntity]:
        query = (
            select(WorkspaceModel)
            .join(WorkspaceMemberModel, WorkspaceModel.id == WorkspaceMemberModel.workspace_id)
            .filter(WorkspaceMemberModel.user_id == member_id)
        )
        result = await self._session.execute(query)
        try:
            workspace_models = result.scalars().all()
        except NoResultFound as error:
            warning(error)
            raise MemberWorkspaceNotFound(f'Участник с id={member_id} не найден.')
        else:
            workspaces = [
                WorkspaceConverter.model_to_entity(workspace) for workspace in workspace_models
            ]
            return workspaces

    async def update(self, workspace: WorkspaceEntity) -> None:
        update_data = WorkspaceConverter.entity_to_dict(workspace)
        stmt = update(WorkspaceModel).filter_by(id=workspace.id).values(**update_data)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise WorkspaceNotUpdated('Рабочее пространство не обновлено')

    async def delete(self, workspace_id: WorkspaceId, owner_id: OwnerId) -> None:
        exists_workspace = await self._session.execute(
            select(
                exists().where(
                    WorkspaceModel.id == workspace_id,
                    WorkspaceModel.owner_id == owner_id,
                )
            )
        )

        if not exists_workspace.scalar():
            raise WorkspaceNotFound(
                f'Рабочее пространство с id={workspace_id} не найдено у этого пользователя.'
            )

        stmt = delete(WorkspaceModel).filter_by(id=workspace_id, owner_id=owner_id)
        await self._session.execute(stmt)

    async def add_member(self, workspace_id: WorkspaceId, user_id: MemberId) -> None:
        stmt = WorkspaceMemberModel(workspace_id=workspace_id, user_id=user_id)
        self._session.add(stmt)
        try:
            await self._session.flush()
        except IntegrityError as error:
            warning(error)
            if isinstance(error.orig.__cause__, ForeignKeyViolationError):
                raise MemberWorkspaceNotFound(f'Участник с id={user_id} не существует')

            raise WorkspaceNotFound(f'Рабочее пространство с id={workspace_id} не найдено')