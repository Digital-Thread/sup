from uuid import UUID

from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.workspace_dtos import WorkspaceAppDTO
from src.apps.workspace.exceptions.workspace_exceptions import (
    WorkspaceException,
    WorkspaceNotFound,
)
from src.apps.workspace.mappers.workspace_mapper import WorkspaceMapper
from src.apps.workspace.repositories.i_workspace_repository import IWorkspaceRepository


class GetWorkspaceByIdUseCase:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, workspace_id: UUID) -> WorkspaceAppDTO | None:
        try:
            workspace = await self._workspace_repository.find_by_id(WorkspaceId(workspace_id))
        except WorkspaceNotFound as error:
            raise WorkspaceException(str(error))
        else:
            return WorkspaceMapper.entity_to_dto(workspace, WorkspaceAppDTO)
