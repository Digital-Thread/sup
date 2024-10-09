from src.apps.workspace.domain.entities.workspace import Workspace
from src.apps.workspace.domain.types_ids import OwnerId
from src.apps.workspace.dtos.workspace_dtos import CreateWorkspaceAppDTO
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceAlreadyExists
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
        except WorkspaceAlreadyExists:
            raise ValueError(f'Рабочее пространство {workspace.name} уже существует')
