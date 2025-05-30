from logging import warning

from asyncpg.exceptions import ForeignKeyViolationError
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
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
from src.data_access.mappers.workspace_mapper import WorkspaceMapper
from src.data_access.models import UserModel, WorkspaceMemberModel, WorkspaceModel


class WorkspaceRepository(IWorkspaceRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def save(self, workspace: WorkspaceEntity) -> None:
        stmt = WorkspaceMapper.entity_to_model(workspace)
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

    async def get_by_id(self, workspace_id: WorkspaceId) -> WorkspaceEntity | None:
        query = select(WorkspaceModel).filter_by(id=workspace_id)
        result = await self._session.execute(query)
        workspace_model = result.scalar_one_or_none()
        workspace_entity = (
            WorkspaceMapper.model_to_entity(workspace_model) if workspace_model else None
        )
        return workspace_entity

    async def get_by_member_id(self, member_id: MemberId) -> list[WorkspaceEntity]:
        query = (
            select(WorkspaceModel)
            .join(WorkspaceMemberModel, WorkspaceModel.id == WorkspaceMemberModel.workspace_id)
            .filter(WorkspaceMemberModel.user_id == member_id)
        )
        result = await self._session.execute(query)
        workspace_models = result.scalars().all()
        workspaces = [WorkspaceMapper.model_to_entity(workspace) for workspace in workspace_models]
        return workspaces

    async def update(self, workspace: WorkspaceEntity) -> None:
        update_data = WorkspaceMapper.entity_to_dict(workspace)
        stmt = update(WorkspaceModel).filter_by(id=workspace.id).values(**update_data)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise WorkspaceNotUpdated('Рабочее пространство не обновлено')

    async def delete(self, workspace_id: WorkspaceId, owner_id: OwnerId) -> None:
        stmt = delete(WorkspaceModel).filter_by(id=workspace_id, owner_id=owner_id)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise WorkspaceNotFound(
                f'Рабочее пространство с id={workspace_id} не найдено у этого пользователя.'
            )

    async def get_workspace_members(self, workspace_id: WorkspaceId) -> dict[MemberId, str]:
        query = (
            select(
                UserModel.id,
                UserModel.first_name,
                UserModel.last_name,
            )
            .join(WorkspaceMemberModel)
            .filter(WorkspaceMemberModel.workspace_id == workspace_id)
        )
        results = await self._session.execute(query)
        members = {member.id: f'{member.first_name} {member.last_name}' for member in results}
        return members

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
