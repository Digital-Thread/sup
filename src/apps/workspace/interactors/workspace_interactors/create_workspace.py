from src.apps.workspace.domain.entities.workspace import WorkspaceEntity
from src.apps.workspace.domain.types_ids import MemberId, OwnerId, WorkspaceId
from src.apps.workspace.dtos.workspace_dtos import CreateWorkspaceDTO
from src.apps.workspace.exceptions.workspace_exceptions import (
    MemberWorkspaceNotFound,
    WorkspaceAlreadyExists,
    WorkspaceException,
)
from src.apps.workspace.repositories.workspace_repository import IWorkspaceRepository


class CreateWorkspaceInteractor:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, create_workspace_data: CreateWorkspaceDTO) -> None:
        try:
            workspace = WorkspaceEntity(
                owner_id=OwnerId(create_workspace_data.owner_id), _name=create_workspace_data.name
            )
        except ValueError as error:
            raise WorkspaceException(f'{str(error)}')

        try:
            await self._workspace_repository.save(workspace)
        except (WorkspaceAlreadyExists, MemberWorkspaceNotFound):
            raise

        await self._add_owner_as_member(workspace.id, workspace.owner_id)

    async def _add_owner_as_member(self, workspace_id: WorkspaceId, owner_id: OwnerId) -> None:
        """Метод для автоматического добавления владельца, как члена рабочего пространства"""
        await self._workspace_repository.add_member(workspace_id, MemberId(owner_id))
