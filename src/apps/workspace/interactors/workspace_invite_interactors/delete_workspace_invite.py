from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId
from src.apps.workspace.dtos.workspace_invite_dtos import DeleteWorkspaceInviteAppDTO
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteException,
    WorkspaceInviteNotFound,
    WorkspaceWorkspaceInviteNotFound,
)
from src.apps.workspace.repositories.workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class DeleteWorkspaceInviteInteractor:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspaceInvite_repository = workspace_invite_repository

    async def execute(self, request_data: DeleteWorkspaceInviteAppDTO) -> None:
        try:
            await self._workspaceInvite_repository.delete(
                InviteId(request_data.id_), WorkspaceId(request_data.workspace_id)
            )
        except (WorkspaceInviteNotFound, WorkspaceWorkspaceInviteNotFound) as error:
            raise WorkspaceInviteException(f'{str(error)}')
