from src.apps.workspace.dtos.workspace_invite_dtos import WorkspaceInviteAppDTO
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteNotUpdated,
)
from src.apps.workspace.mappers.workspace_invite_mapper import WorkspaceInviteMapper
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class UpdateWorkspaceInviteUseCase:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspace_invite_repository = workspace_invite_repository

    async def execute(self, update_data: WorkspaceInviteAppDTO) -> None:
        workspace_invite = WorkspaceInviteMapper.dto_to_entity(update_data)

        try:
            await self._workspace_invite_repository.update(workspace_invite)
        except WorkspaceInviteNotUpdated:
            pass
            # TODO пробросить дальше
