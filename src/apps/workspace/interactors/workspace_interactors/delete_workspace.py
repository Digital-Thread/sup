from uuid import UUID

from src.apps.workspace.domain.types_ids import OwnerId, WorkspaceId
from src.apps.workspace.exceptions.workspace_exceptions import (
    WorkspaceException,
    WorkspaceNotFound,
)
from src.apps.workspace.repositories.workspace_repository import IWorkspaceRepository


class DeleteWorkspaceInteractor:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, workspace_id: UUID, owner_id: UUID) -> None:
        try:
            await self._workspace_repository.delete(WorkspaceId(workspace_id), OwnerId(owner_id))
        except WorkspaceNotFound as error:
            raise WorkspaceException(f'{str(error)}')
