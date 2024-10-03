from uuid import UUID

from src.apps.workspace.domain.entities.workspace import Workspace
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceNotFound
from src.apps.workspace.repositories.i_workspace_repository import IWorkspaceRepository


class GetWorkspaceById:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, workspace_id: UUID) -> Workspace:
        try:
            workspace = await self._workspace_repository.find_by_id(workspace_id)
        except WorkspaceNotFound:
            raise ValueError(f'Рабочее пространство с id={workspace_id} не найдено')

        return workspace
