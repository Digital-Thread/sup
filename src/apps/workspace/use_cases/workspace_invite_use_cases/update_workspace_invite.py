from src.apps.workspace.domain.types_ids import InviteId
from src.apps.workspace.dtos.workspace_invite_dtos import UpdateWorkspaceInviteAppDTO
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteNotFound,
    WorkspaceInviteNotUpdated,
)
from src.apps.workspace.mappers.workspace_invite_mapper import WorkspaceInviteMapper
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class UpdateWorkspaceInviteUseCase:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspace_invite_repository = workspace_invite_repository

    async def execute(self, invite_id: InviteId, update_data: UpdateWorkspaceInviteAppDTO) -> None:
        try:
            existing_invite = await self._workspace_invite_repository.find_by_id(invite_id)
        except WorkspaceInviteNotFound:
            pass
            # TODO пробросить дальше
        else:
            updated_invite = WorkspaceInviteMapper.update_data(existing_invite, update_data)

            try:
                await self._workspace_invite_repository.update(updated_invite)
            except WorkspaceInviteNotUpdated:
                pass
                # TODO пробросить дальше
