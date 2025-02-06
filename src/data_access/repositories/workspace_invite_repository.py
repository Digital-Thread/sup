from logging import warning
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.workspace.domain.entities.workspace_invite import WorkspaceInviteEntity
from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteNotFound,
    WorkspaceInviteNotUpdated,
    WorkspaceWorkspaceInviteNotFound,
)
from src.apps.workspace.repositories.workspace_invite_repository import (
    IWorkspaceInviteRepository,
)
from src.data_access.mappers.workspace_invite_mapper import WorkspaceInviteMapper
from src.data_access.models.workspace_models.workspace_invite import (
    WorkspaceInviteModel,
)


class WorkspaceInviteRepository(IWorkspaceInviteRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def save(self, workspace_invite: WorkspaceInviteEntity) -> None:
        stmt = WorkspaceInviteMapper.entity_to_model(workspace_invite)
        self._session.add(stmt)

        try:
            await self._session.flush()
        except IntegrityError as error:
            warning(error)
            raise WorkspaceWorkspaceInviteNotFound(
                f'Рабочего пространства с id={workspace_invite.workspace_id} не существует'
            )

    async def get_by_id(
        self, workspace_invite_id: InviteId, workspace_id: WorkspaceId | None = None
    ) -> WorkspaceInviteEntity | None:
        query = select(WorkspaceInviteModel).filter_by(
            id=workspace_invite_id, workspace_id=workspace_id
        )
        result = await self._session.execute(query)
        invite_model = result.scalar_one_or_none()
        return WorkspaceInviteMapper.model_to_entity(invite_model) if invite_model else None

    async def get_by_workspace_id(self, workspace_id: WorkspaceId, page: int, page_size: int) -> list[WorkspaceInviteEntity]:
        query = select(WorkspaceInviteModel).filter_by(workspace_id=workspace_id).limit(page_size).offset((page- 1) * page_size)
        result = await self._session.execute(query)
        invites = [
            WorkspaceInviteMapper.model_to_entity(invite) for invite in result.scalars().all()
        ]

        return invites

    async def get_by_code(self, code: UUID) -> tuple[WorkspaceId, InviteId]:
        query = select(WorkspaceInviteModel.workspace_id, WorkspaceInviteModel.id).filter_by(
            code=code
        )
        result = await self._session.execute(query)
        workspace_and_invite_ids = result.fetchone()
        return workspace_and_invite_ids[0], workspace_and_invite_ids[1]

    async def update(self, workspace_invite: WorkspaceInviteEntity) -> None:
        update_data = WorkspaceInviteMapper.entity_to_dict(workspace_invite)
        stmt = update(WorkspaceInviteModel).filter_by(id=workspace_invite.id).values(**update_data)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise WorkspaceInviteNotUpdated(
                f'Ссылка приглашения с id={workspace_invite.id} не обновлена'
            )

    async def delete(self, workspace_invite_id: InviteId, workspace_id: WorkspaceId) -> None:
        stmt = delete(WorkspaceInviteModel).filter_by(
            id=workspace_invite_id, workspace_id=workspace_id
        )
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise WorkspaceInviteNotFound(
                f'Ссылка приглашения с id={workspace_invite_id} не найдена в рабочем пространстве при удалении.'
            )
