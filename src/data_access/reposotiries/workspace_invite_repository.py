from logging import warning
from typing import Optional
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.workspace.domain.entities.workspace_invite import WorkspaceInvite
from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteCreatedException,
    WorkspaceInviteNotDeleted,
    WorkspaceInviteNotUpdated,
)
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)
from src.data_access.converters.workspace_invite_converter import (
    WorkspaceInviteConverter,
)
from src.data_access.models.workspace_models.workspace_invite import (
    WorkspaceInviteModel,
)


class WorkspaceInviteRepository(IWorkspaceInviteRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def save(self, workspace_invite: WorkspaceInvite) -> None:
        stmt = WorkspaceInviteConverter.entity_to_model(workspace_invite)
        self._session.add(stmt)

        try:
            await self._session.flush()
        except IntegrityError as error:
            warning(error)
            raise WorkspaceInviteCreatedException('Ошибка создания ссылки приглашения')

    async def find_by_id(self, workspace_invite_id: InviteId) -> Optional[WorkspaceInvite]:
        query = await self._session.get(WorkspaceInviteModel, workspace_invite_id)
        workspace_invite = WorkspaceInviteConverter.model_to_entity(query)
        return workspace_invite

    async def find_by_workspace_id(self, workspace_id: WorkspaceId) -> list[WorkspaceInvite]:
        query = select(WorkspaceInviteModel).filter_by(workspace_id=workspace_id)
        result = await self._session.execute(query)
        categories = [
            WorkspaceInviteConverter.model_to_entity(workspace_invite)
            for workspace_invite in result.scalars().all()
        ]
        return categories

    async def update(self, workspace_invite: WorkspaceInvite) -> None:
        model = WorkspaceInviteConverter.entity_to_model(workspace_invite)
        stmt = update(WorkspaceInviteModel).filter_by(id=model.id).values(**model.__dict__)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise WorkspaceInviteNotUpdated(f'Ссылка приглашения с id={model.id} не обновлена')

    async def delete(self, workspace_invite_id: InviteId) -> None:
        stmt = delete(WorkspaceInviteModel).filter_by(id=workspace_invite_id)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise WorkspaceInviteNotDeleted(
                f'Ссылка приглашения с id={workspace_invite_id} не удалена'
            )
