from uuid import UUID

from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.workspace_dtos import MemberOutDTO
from src.apps.workspace.mappers.workspace_mapper import WorkspaceMapper
from src.apps.workspace.repositories import IWorkspaceRepository


class GetWorkspaceMembersInteractor:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, workspace_id: UUID) -> list[MemberOutDTO]:
        members_dict = await self._workspace_repository.get_workspace_members(
            workspace_id=WorkspaceId(workspace_id)
        )
        members_out_dto = WorkspaceMapper.dict_to_dto(members_dict)
        return members_out_dto
