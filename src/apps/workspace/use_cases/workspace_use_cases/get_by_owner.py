from uuid import UUID

from src.apps.workspace.dtos.workspace_dtos import WorkspaceAppDTO
from src.apps.workspace.exceptions.workspace_exceptions import OwnerWorkspaceNotFound
from src.apps.workspace.repositories.i_workspace_repository import IWorkspaceRepository


class GetWorkspaceByOwnerUseCase:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, owner_id: UUID) -> list[WorkspaceAppDTO]:
        try:
            workspaces = await self._workspace_repository.find_by_owner_id(owner_id)
        except OwnerWorkspaceNotFound:
            raise ValueError(f'Владелец рабочего пространства с id={owner_id}')
        else:
            return [WorkspaceAppDTO.from_entity(workspace) for workspace in workspaces]
