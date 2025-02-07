from uuid import UUID

from src.apps.workspace.domain.entities.workspace_invite import WorkspaceInviteEntity
from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceWorkspaceInviteNotFound,
)
from src.apps.workspace.repositories.workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class CreateWorkspaceInviteInteractor:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspaceInvite_repository = workspace_invite_repository

    async def execute(self, workspace_id: UUID) -> None:
        try:
            await self._workspaceInvite_repository.save(
                WorkspaceInviteEntity(_workspace_id=WorkspaceId(workspace_id))
            )
        except WorkspaceWorkspaceInviteNotFound:
            raise
