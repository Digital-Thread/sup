from uuid import UUID

from src.apps.workspace.domain.types_ids import OwnerId
from src.apps.workspace.dtos.workspace_dtos import WorkspaceAppDTO
from src.apps.workspace.exceptions.workspace_exceptions import OwnerWorkspaceNotFound
from src.apps.workspace.mappers.category_mapper import CategoryMapper
from src.apps.workspace.mappers.workspace_mapper import WorkspaceMapper
from src.apps.workspace.repositories.i_workspace_repository import IWorkspaceRepository


class GetWorkspaceByOwnerUseCase:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, owner_id: OwnerId) -> list[WorkspaceAppDTO]:
        try:
            workspaces = await self._workspace_repository.find_by_owner_id(owner_id)
        except OwnerWorkspaceNotFound:
            raise ValueError(f'Владелец рабочего пространства с id={owner_id}')
        else:
            return [
                WorkspaceMapper.entity_to_dto(workspace, WorkspaceAppDTO)
                for workspace in workspaces
            ]
