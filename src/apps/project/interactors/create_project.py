from src.apps.project.dtos import ProjectCreateDTO
from src.apps.project.exceptions import (
    ProjectAlreadyExists,
    ProjectException,
    WorkspaceForProjectNotFound,
)
from src.apps.project.project_repository import IProjectRepository
from src.apps.project.mapper import ProjectMapper


class CreateProjectInteractor:
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository

    async def execute(self, project_data: ProjectCreateDTO) -> None:
        try:
            await self._project_repository.save(ProjectMapper.dto_to_entity(project_data))
        except (ValueError, WorkspaceForProjectNotFound, ProjectAlreadyExists) as error:
            raise ProjectException(f'{str(error)}')
