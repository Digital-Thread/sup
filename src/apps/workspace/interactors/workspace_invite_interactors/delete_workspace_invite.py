from src.apps.workspace.domain.types_ids import InviteId
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

    async def execute(self, workspace_invite: int) -> None:
        try:
            await self._workspaceInvite_repository.delete(InviteId(workspace_invite))
        except (WorkspaceInviteNotFound, WorkspaceWorkspaceInviteNotFound) as error:
            raise WorkspaceInviteException(f'{str(error)}')
