from src.apps.project.domain.types_ids import ProjectId
from src.apps.project.exceptions import (
    ProjectException,
    ProjectNotDeleted,
)
from src.apps.project.project_repository import IProjectRepository


class DeleteProjectInteractor:
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository

    async def execute(self, project_id: int) -> None:
        try:
            await self._project_repository.delete(ProjectId(project_id))
        except ProjectNotDeleted as error:
            raise ProjectException(str(error)) from error
