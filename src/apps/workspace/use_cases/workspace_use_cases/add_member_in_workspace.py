from uuid import UUID

from src.apps.workspace.domain.types_ids import MemberId, WorkspaceId
from src.apps.workspace.repositories import IWorkspaceRepository


class AddMemberInWorkspaceUseCase:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, workspace_id: UUID, member_id: UUID):
        await self._workspace_repository.add_member(WorkspaceId(workspace_id), MemberId(member_id))
