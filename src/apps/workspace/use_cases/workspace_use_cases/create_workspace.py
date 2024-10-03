from src.apps.workspace.domain.entities.workspace import Workspace
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceAlreadyExists
from src.apps.workspace.repositories.i_workspace_repository import IWorkspaceRepository


class CreateWorkspaceUseCase:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self._workspace_repository = workspace_repository

    async def execute(self, workspace: Workspace) -> None:
        try:
            await self._workspace_repository.save(workspace)
        except WorkspaceAlreadyExists:
            raise ValueError(f'Рабочее пространство {workspace.name} уже существует')
