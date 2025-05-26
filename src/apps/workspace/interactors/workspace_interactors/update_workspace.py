from src.apps.workspace.domain.entities.workspace import WorkspaceEntity
from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.workspace_dtos import (
    OptionalWorkspaceUpdateFields,
    UpdateWorkspaceDTO,
)
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

    async def execute(self, workspace_update_data: UpdateWorkspaceDTO) -> None:
        existing_workspace = await self._get_existing_workspace_by_id(
            workspace_id=WorkspaceId(workspace_update_data.workspace_id)
        )
        updated_workspace = await self._map_to_update_data(
            workspace=existing_workspace, updated_data=workspace_update_data.updated_fields
        )

        try:
            await self._workspace_repository.update(updated_workspace)
        except WorkspaceNotUpdated as error:
            raise WorkspaceException(str(error))

    async def _get_existing_workspace_by_id(self, workspace_id: WorkspaceId) -> WorkspaceEntity:
        existing_workspace = await self._workspace_repository.get_by_id(workspace_id)
        if not existing_workspace:
            raise WorkspaceNotFound(
                f'Рабочее пространство с id={workspace_id} не найдено при обновлении.'
            )

        return existing_workspace

    @staticmethod
    async def _map_to_update_data(
        workspace: WorkspaceEntity, updated_data: OptionalWorkspaceUpdateFields
    ) -> WorkspaceEntity:
        try:
            updated_workspace = WorkspaceMapper.update_data(
                updated_fields=updated_data, existing_workspace=workspace
            )
        except ValueError as error:
            raise WorkspaceException(str(error))
        else:
            return updated_workspace
