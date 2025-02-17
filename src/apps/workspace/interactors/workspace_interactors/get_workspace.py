from uuid import UUID

from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.workspace_dtos import WorkspaceOutDTO
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceNotFound
from src.apps.workspace.mappers.workspace_mapper import WorkspaceMapper
from src.apps.workspace.repositories.workspace_repository import IWorkspaceRepository


class GetWorkspaceByIdInteractor:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, workspace_id: UUID) -> WorkspaceOutDTO:
        workspace_entity = await self._workspace_repository.get_by_id(WorkspaceId(workspace_id))
        try:
            workspace_out_dto = WorkspaceMapper.entity_to_dto(workspace_entity)
        except AttributeError as error:
            raise WorkspaceNotFound(
                f'Рабочее пространство с id={workspace_id} не найдено'
            ) from error

        return workspace_out_dto
