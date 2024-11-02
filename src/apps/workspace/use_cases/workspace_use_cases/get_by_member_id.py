from uuid import UUID

from src.apps.workspace.domain.types_ids import MemberId
from src.apps.workspace.dtos.workspace_dtos import WorkspaceAppDTO
from src.apps.workspace.exceptions.workspace_exceptions import (
    MemberWorkspaceNotFound,
    WorkspaceException,
)
from src.apps.workspace.mappers.workspace_mapper import WorkspaceMapper
from src.apps.workspace.repositories.i_workspace_repository import IWorkspaceRepository


class GetWorkspaceByMemberUseCase:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, member_id: UUID) -> list[WorkspaceAppDTO]:
        try:
            workspaces = await self._workspace_repository.find_by_member_id(MemberId(member_id))
        except MemberWorkspaceNotFound as error:
            raise WorkspaceException(f'{str(error)}')
        else:
            return [
                WorkspaceMapper.entity_to_dto(workspace, WorkspaceAppDTO)
                for workspace in workspaces
            ]
