from src.apps.workspace.domain.types_ids import MemberId
from src.apps.workspace.repositories import IWorkspaceRepository


class GetWorkspaceMembersInteractor:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self) -> dict[MemberId, str]:
        members = await self._workspace_repository.find_workspace_members()
        return members