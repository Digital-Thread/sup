from logging import warning

from sqlalchemy import delete, exists, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.workspace.domain.entities.workspace_invite import WorkspaceInvite
from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteNotFound,
    WorkspaceInviteNotUpdated,
    WorkspaceWorkspaceInviteNotFound,
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
            raise WorkspaceWorkspaceInviteNotFound(
                f'Рабочего пространства с id={workspace_invite.workspace_id} не существует'
            )

    async def find_by_id(
        self, workspace_invite_id: InviteId, workspace_id: WorkspaceId
    ) -> WorkspaceInvite | None:
        query: WorkspaceInviteModel | None = await self._session.get(
            WorkspaceInviteModel, workspace_invite_id
        )
        workspace_invite = WorkspaceInviteConverter.model_to_entity(query) if query else None
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
        update_data = WorkspaceInviteConverter.entity_to_dict(workspace_invite)
        stmt = update(WorkspaceInviteModel).filter_by(id=workspace_invite.id).values(**update_data)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise WorkspaceInviteNotUpdated(
                f'Ссылка приглашения с id={workspace_invite.id} не обновлена'
            )

    async def delete(self, workspace_invite_id: InviteId, workspace_id: WorkspaceId) -> None:
        exists_workspace_invite = await self._session.execute(
            select(
                exists().where(
                    WorkspaceInviteModel.id == workspace_invite_id,
                    WorkspaceInviteModel.workspace_id == workspace_id,
                )
            )
        )

        if not exists_workspace_invite.scalar():
            raise WorkspaceInviteNotFound(
                f'Ссылка приглашения с id={workspace_invite_id} не найдена в рабочем пространстве'
            )

        stmt = delete(WorkspaceInviteModel).filter_by(
            id=workspace_invite_id, workspace_id=workspace_id
        )
        await self._session.execute(stmt)
