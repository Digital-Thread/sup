from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteException,
    WorkspaceInviteNotFound,
    WorkspaceWorkspaceInviteNotFound,
)
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class DeleteWorkspaceInviteUseCase:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspaceInvite_repository = workspace_invite_repository

    async def execute(self, invite_id: InviteId, workspace_id: WorkspaceId) -> None:
        try:
            await self._workspaceInvite_repository.delete(invite_id, workspace_id)
        except (WorkspaceInviteNotFound, WorkspaceWorkspaceInviteNotFound) as error:
            raise WorkspaceInviteException(f'{str(error)}')
