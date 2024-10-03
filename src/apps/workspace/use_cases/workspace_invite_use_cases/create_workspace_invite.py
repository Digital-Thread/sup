from src.apps.workspace.domain.entities.workspace_invite import WorkspaceInvite
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteAlreadyExists,
)
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class CreateWorkspaceInviteUseCase:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspaceInvite_repository = workspace_invite_repository

    async def execute(self, workspace_invite: WorkspaceInvite) -> None:
        try:
            await self._workspaceInvite_repository.save(workspace_invite)
        except WorkspaceInviteAlreadyExists:
            raise ValueError(f'Ссылка приглашения {workspace_invite.code} уже существует')
