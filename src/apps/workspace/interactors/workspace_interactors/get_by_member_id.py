from src.apps.workspace.domain.types_ids import MemberId
from src.apps.workspace.dtos.workspace_dtos import (
    GetWorkspacesByMemberIdDTO,
    WorkspaceOutDTO,
)
from src.apps.workspace.exceptions.workspace_exceptions import MemberWorkspaceNotFound
from src.apps.workspace.mappers.workspace_mapper import WorkspaceMapper
from src.apps.workspace.repositories.workspace_repository import IWorkspaceRepository


class GetWorkspaceByMemberInteractor:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, request_data: GetWorkspacesByMemberIdDTO) -> list[WorkspaceOutDTO]:
        try:
            workspaces = await self._workspace_repository.get_by_member_id(
                MemberId(request_data.member_id)
            )
        except MemberWorkspaceNotFound:
            raise
        else:
            return [WorkspaceMapper.entity_to_dto(workspace) for workspace in workspaces]
