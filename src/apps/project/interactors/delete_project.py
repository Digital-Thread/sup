from uuid import UUID

from src.apps.project.domain.types_ids import ProjectId, WorkspaceId
from src.apps.project.exceptions import (
    ProjectException,
    ProjectNotFound,
    WorkspaceForProjectNotFound,
)
from src.apps.project.project_repository import IProjectRepository


class DeleteProjectInteractor:
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository

    async def execute(self, project_id: int, workspace_id: UUID) -> None:
        try:
            await self._project_repository.delete(ProjectId(project_id), WorkspaceId(workspace_id))
        except (ProjectNotFound, WorkspaceForProjectNotFound) as error:
            raise ProjectException(f'{str(error)}')
