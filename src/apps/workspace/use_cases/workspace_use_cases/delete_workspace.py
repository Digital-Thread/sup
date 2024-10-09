from uuid import UUID

from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceNotFound
from src.apps.workspace.repositories.i_workspace_repository import IWorkspaceRepository


class DeleteWorkspaceUseCase:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, workspace_id: WorkspaceId) -> None:
        try:
            await self._workspace_repository.delete(workspace_id)
        except WorkspaceNotFound:
            ValueError(f'Рабочего пространства с id={workspace_id} не существует')
