from src.apps.workspace.domain.types_ids import OwnerId, WorkspaceId
from src.apps.workspace.exceptions.workspace_exceptions import (
    WorkspaceException,
    WorkspaceNotFound,
)
from src.apps.workspace.repositories.i_workspace_repository import IWorkspaceRepository


class DeleteWorkspaceUseCase:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, workspace_id: WorkspaceId, owner_id: OwnerId) -> None:
        try:
            await self._workspace_repository.delete(workspace_id, owner_id)
        except WorkspaceNotFound as error:
            raise WorkspaceException(f'{str(error)}')
