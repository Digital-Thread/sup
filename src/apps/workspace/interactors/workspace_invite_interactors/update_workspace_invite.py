from src.apps.workspace.domain.entities.workspace_invite import WorkspaceInviteEntity
from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId
from src.apps.workspace.dtos.workspace_invite_dtos import UpdateWorkspaceInviteAppDTO
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteException,
    WorkspaceInviteNotFound,
    WorkspaceInviteNotUpdated,
    WorkspaceWorkspaceInviteNotFound,
)
from src.apps.workspace.mappers.workspace_invite_mapper import WorkspaceInviteMapper
from src.apps.workspace.repositories.workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class UpdateWorkspaceInviteInteractor:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspace_invite_repository = workspace_invite_repository

    async def execute(
        self, request_data: UpdateWorkspaceInviteAppDTO) -> None:
        existing_invite = await self._get_existing_invite_in_workspace(
            InviteId(request_data.id_), WorkspaceId(request_data.workspace_id)
        )
        updated_invite = self._map_to_update_data(existing_invite, request_data)
        try:
            await self._workspace_invite_repository.update(updated_invite)
        except WorkspaceInviteNotUpdated as error:
            raise WorkspaceInviteException(f'{str(error)}')

    async def _get_existing_invite_in_workspace(
        self, invite_id: InviteId, workspace_id: WorkspaceId
    ) -> WorkspaceInviteEntity:
        try:
            existing_invite = await self._workspace_invite_repository.find_by_id(
                invite_id, workspace_id
            )
        except (WorkspaceWorkspaceInviteNotFound, WorkspaceInviteNotFound) as error:
            raise WorkspaceInviteException(f'{str(error)}')
        else:
            return existing_invite

    @staticmethod
    def _map_to_update_data(
        invite: WorkspaceInviteEntity, update_data: UpdateWorkspaceInviteAppDTO
    ) -> WorkspaceInviteEntity:
        try:
            updated_invite = WorkspaceInviteMapper.update_data(invite, update_data)
        except ValueError as error:
            raise WorkspaceInviteException(f'{str(error)}')
        else:
            return updated_invite
