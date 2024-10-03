from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteNotFound,
)
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class DeleteWorkspaceInviteUseCase:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspaceInvite_repository = workspace_invite_repository

    async def execute(self, workspace_invite_id: int) -> None:
        try:
            await self._workspaceInvite_repository.delete(workspace_invite_id)
        except WorkspaceInviteNotFound:
            ValueError(f'Ссылка приглашения с id={workspace_invite_id} не существует')
