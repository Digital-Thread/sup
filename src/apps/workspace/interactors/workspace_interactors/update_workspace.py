from src.apps.workspace.domain.entities.workspace import WorkspaceEntity
from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.workspace_dtos import UpdateWorkspaceAppDTO
from src.apps.workspace.exceptions.workspace_exceptions import (
    WorkspaceException,
    WorkspaceNotFound,
    WorkspaceNotUpdated,
)
from src.apps.workspace.mappers.workspace_mapper import WorkspaceMapper
from src.apps.workspace.repositories.workspace_repository import IWorkspaceRepository


class UpdateWorkspaceInteractor:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, request_data: UpdateWorkspaceAppDTO) -> None:
        updated_workspace = await self._map_to_update_data(WorkspaceId(request_data.id), request_data)
        try:
            await self._workspace_repository.update(updated_workspace)
        except WorkspaceNotUpdated as error:
            raise WorkspaceException(str(error))

    async def _get_existing_workspace_by_id(self, workspace_id: WorkspaceId) -> WorkspaceEntity:
        try:
            existing_workspace = await self._workspace_repository.find_by_id(workspace_id)
        except WorkspaceNotFound as error:
            raise WorkspaceException(f'{str(error)} при попытке обновить')
        else:
            return existing_workspace

    async def _map_to_update_data(
        self, workspace_id: WorkspaceId, updated_data: UpdateWorkspaceAppDTO
    ) -> WorkspaceEntity:
        existing_workspace = await self._get_existing_workspace_by_id(workspace_id)
        try:
            updated_workspace = WorkspaceMapper.update_data(updated_data, existing_workspace)
        except ValueError as error:
            raise WorkspaceException(f'{str(error)} при попытке обновить')
        else:
            return updated_workspace
