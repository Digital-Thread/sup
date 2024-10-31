from src.apps.project.domain.types_ids import ProjectId, WorkspaceId
from src.apps.project.exceptions import (
    ProjectException,
    ProjectNotFound,
    WorkspaceForProjectNotFound,
)
from src.apps.project.i_project_repository import IProjectRepository


class DeleteProjectUseCase:
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository

    async def execute(self, project_id: ProjectId, workspace_id: WorkspaceId) -> None:
        try:
            await self._project_repository.delete(project_id, workspace_id)
        except (ProjectNotFound, WorkspaceForProjectNotFound) as error:
            raise ProjectException(f'{str(error)}')
