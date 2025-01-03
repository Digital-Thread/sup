from uuid import UUID

from src.apps.workspace.domain.entities.workspace_invite import WorkspaceInvite
from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteException,
    WorkspaceWorkspaceInviteNotFound,
)
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class CreateWorkspaceInviteUseCase:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspaceInvite_repository = workspace_invite_repository

    async def execute(self, workspace_id: UUID) -> None:
        try:
            await self._workspaceInvite_repository.save(
                WorkspaceInvite(_workspace_id=WorkspaceId(workspace_id))
            )
        except WorkspaceWorkspaceInviteNotFound as error:
            raise WorkspaceInviteException(f'{str(error)}')
