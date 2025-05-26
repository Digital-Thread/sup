from src.apps.workspace.domain.types_ids import OwnerId, WorkspaceId
from src.apps.workspace.dtos.workspace_dtos import DeleteWorkspaceDTO
from src.apps.workspace.exceptions.workspace_exceptions import (
    WorkspaceException,
    WorkspaceNotFound,
)
from src.apps.workspace.repositories.workspace_repository import IWorkspaceRepository


class DeleteWorkspaceInteractor:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, workspace_deletion_data: DeleteWorkspaceDTO) -> None:
        try:
            await self._workspace_repository.delete(
                WorkspaceId(workspace_deletion_data.workspace_id),
                OwnerId(workspace_deletion_data.owner_id),
            )
        except WorkspaceNotFound as error:
            raise WorkspaceException(f'{str(error)}')
