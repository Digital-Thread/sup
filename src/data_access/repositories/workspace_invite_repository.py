from logging import warning
from uuid import UUID

from sqlalchemy import delete, exists, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
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
from src.data_access.mappers.workspace_invite_mapper import (
    WorkspaceInviteMapper,
)
from src.data_access.models.workspace_models.workspace_invite import (
    WorkspaceInviteModel,
)
from src.providers.context import WorkspaceContext


class WorkspaceInviteRepository(IWorkspaceInviteRepository):
    def __init__(self, session_factory: AsyncSession, context: WorkspaceContext):
        self._session = session_factory
        self._context = context

    async def save(self, workspace_invite: WorkspaceInviteEntity) -> None:
        workspace_invite.workspace_id = self._context.workspace_id
        stmt = WorkspaceInviteMapper.entity_to_model(workspace_invite)
        self._session.add(stmt)

        try:
            await self._session.flush()
        except IntegrityError as error:
            warning(error)
            raise WorkspaceWorkspaceInviteNotFound(
                f'Рабочего пространства с id={workspace_invite.workspace_id} не существует'
            )

    async def get_by_id(self, workspace_invite_id: InviteId) -> WorkspaceInviteEntity | None:
        query = select(WorkspaceInviteModel).filter_by(
            id=workspace_invite_id, workspace_id=self._context.workspace_id
        )
        result = await self._session.execute(query)
        try:
            invite_model = result.scalar_one()
        except NoResultFound as error:
            warning(error)
            raise WorkspaceInviteNotFound(
                f'Ссылка приглашения с id={workspace_invite_id} не найдена в указанном рабочем пространстве.'
            )
        else:
            return WorkspaceInviteMapper.model_to_entity(invite_model)

    async def get_by_workspace_id(self) -> list[WorkspaceInviteEntity]:
        query = select(WorkspaceInviteModel).filter_by(workspace_id=self._context.workspace_id)
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

    async def delete(self, workspace_invite_id: InviteId) -> None:
        exists_workspace_invite = await self._session.execute(
            select(
                exists().where(
                    WorkspaceInviteModel.id == workspace_invite_id,
                    WorkspaceInviteModel.workspace_id == self._context.workspace_id,
                )
            )
        )

        if not exists_workspace_invite.scalar():
            raise WorkspaceInviteNotFound(
                f'Ссылка приглашения с id={workspace_invite_id} не найдена в рабочем пространстве при удалении.'
            )

        stmt = delete(WorkspaceInviteModel).filter_by(
            id=workspace_invite_id, workspace_id=self._context.workspace_id
        )
        await self._session.execute(stmt)
