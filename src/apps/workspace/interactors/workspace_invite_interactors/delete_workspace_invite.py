from uuid import UUID

from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteNotFound,
    WorkspaceWorkspaceInviteNotFound,
)
from src.apps.workspace.repositories.workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class DeleteWorkspaceInviteInteractor:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspaceInvite_repository = workspace_invite_repository

    async def execute(self, workspace_invite_id: int, workspace_id: UUID) -> None:
        try:
            await self._workspaceInvite_repository.delete(
                InviteId(workspace_invite_id), WorkspaceId(workspace_id)
            )
        except (WorkspaceInviteNotFound, WorkspaceWorkspaceInviteNotFound):
            raise
