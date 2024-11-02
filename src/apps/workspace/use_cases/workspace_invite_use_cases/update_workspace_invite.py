from uuid import UUID

from src.apps.workspace.domain.entities.workspace_invite import WorkspaceInvite
from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId
from src.apps.workspace.dtos.workspace_invite_dtos import UpdateWorkspaceInviteAppDTO
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteException,
    WorkspaceInviteNotUpdated,
    WorkspaceWorkspaceInviteNotFound,
)
from src.apps.workspace.mappers.workspace_invite_mapper import WorkspaceInviteMapper
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class UpdateWorkspaceInviteUseCase:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspace_invite_repository = workspace_invite_repository

    async def execute(
        self,
        invite_id: int,
        workspace_id: UUID,
        update_data: UpdateWorkspaceInviteAppDTO,
    ) -> None:
        existing_invite = await self._get_existing_invite_in_workspace(
            InviteId(invite_id), WorkspaceId(workspace_id)
        )
        updated_invite = self._map_to_update_data(existing_invite, update_data)
        try:
            await self._workspace_invite_repository.update(updated_invite)
        except WorkspaceInviteNotUpdated as error:
            raise WorkspaceInviteException(f'{str(error)}')

    async def _get_existing_invite_in_workspace(
        self, invite_id: InviteId, workspace_id: WorkspaceId
    ) -> WorkspaceInvite:
        try:
            existing_invite = await self._workspace_invite_repository.find_by_id(
                invite_id, workspace_id
            )
        except WorkspaceWorkspaceInviteNotFound as error:
            raise WorkspaceInviteException(f'{str(error)}')
        else:
            return existing_invite

    @staticmethod
    def _map_to_update_data(
        invite: WorkspaceInvite, update_data: UpdateWorkspaceInviteAppDTO
    ) -> WorkspaceInvite:
        try:
            updated_invite = WorkspaceInviteMapper.update_data(invite, update_data)
        except ValueError as error:
            raise WorkspaceInviteException(f'{str(error)}')
        else:
            return updated_invite
