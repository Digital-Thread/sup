from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.workspace_dtos import WorkspaceAppDTO, GetWorkspaceAppDTO
from src.apps.workspace.exceptions.workspace_exceptions import (
    WorkspaceException,
    WorkspaceNotFound,
)
from src.apps.workspace.mappers.workspace_mapper import WorkspaceMapper
from src.apps.workspace.repositories.workspace_repository import IWorkspaceRepository


class GetWorkspaceByIdInteractor:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, request_data: GetWorkspaceAppDTO) -> WorkspaceAppDTO | None:
        try:
            workspace = await self._workspace_repository.find_by_id(WorkspaceId(request_data.id))
        except WorkspaceNotFound as error:
            raise WorkspaceException(str(error))
        else:
            return WorkspaceMapper.entity_to_dto(workspace, WorkspaceAppDTO)
