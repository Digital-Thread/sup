from uuid import UUID

from src.apps.workspace.domain.types_ids import MemberId, WorkspaceId
from src.apps.workspace.repositories import IWorkspaceRepository


class GetWorkspaceMembersInteractor:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, workspace_id: UUID) -> dict[MemberId, str]:
        members = await self._workspace_repository.find_workspace_members(WorkspaceId(workspace_id))
        return members