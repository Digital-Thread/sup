from src.apps.workspace.domain.types_ids import OwnerId, WorkspaceId
from src.apps.workspace.dtos.workspace_dtos import DeleteWorkspaceAppDTO
from src.apps.workspace.exceptions.workspace_exceptions import (
    WorkspaceException,
    WorkspaceNotFound,
)
from src.apps.workspace.repositories.workspace_repository import IWorkspaceRepository


class DeleteWorkspaceInteractor:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, request_data: DeleteWorkspaceAppDTO) -> None:
        try:
            await self._workspace_repository.delete(WorkspaceId(request_data.id), OwnerId(request_data.owner_id))
        except WorkspaceNotFound as error:
            raise WorkspaceException(f'{str(error)}')
