from src.apps.workspace.domain.entities.workspace import Workspace
from src.apps.workspace.domain.types_ids import OwnerId, WorkspaceId, MemberId
from src.apps.workspace.dtos.workspace_dtos import CreateWorkspaceAppDTO
from src.apps.workspace.exceptions.workspace_exceptions import (
    OwnerWorkspaceNotFound,
    WorkspaceAlreadyExists,
    WorkspaceException,
)
from src.apps.workspace.repositories.i_workspace_repository import IWorkspaceRepository


class CreateWorkspaceUseCase:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, workspace_data: CreateWorkspaceAppDTO) -> None:
        workspace = Workspace(
            owner_id=OwnerId(workspace_data['owner_id']), _name=workspace_data['name']
        )

        try:
            await self._workspace_repository.save(workspace)
        except (WorkspaceAlreadyExists, OwnerWorkspaceNotFound) as error:
            raise WorkspaceException(f'{str(error)}')
        else:
            await self._add_owner_as_member(workspace.id, workspace.owner_id)

    async def _add_owner_as_member(self, workspace_id: WorkspaceId, owner_id: OwnerId) -> None:
        """Метод для автоматического добавления пользователя, как члена рабочего пространства"""
        await self._workspace_repository.add_member(workspace_id, MemberId(owner_id))