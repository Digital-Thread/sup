from src.apps.workspace.domain.types_ids import OwnerId
from src.apps.workspace.dtos.workspace_dtos import WorkspaceAppDTO
from src.apps.workspace.exceptions.workspace_exceptions import (
    OwnerWorkspaceNotFound,
    WorkspaceException,
)
from src.apps.workspace.mappers.workspace_mapper import WorkspaceMapper
from src.apps.workspace.repositories.i_workspace_repository import IWorkspaceRepository


class GetWorkspaceByOwnerUseCase:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, owner_id: OwnerId) -> list[WorkspaceAppDTO]:
        try:
            workspaces = await self._workspace_repository.find_by_owner_id(owner_id)
        except OwnerWorkspaceNotFound as error:
            raise WorkspaceException(f'{str(error)}')
        else:
            return [
                WorkspaceMapper.entity_to_dto(workspace, WorkspaceAppDTO)
                for workspace in workspaces
            ]
