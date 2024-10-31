from src.apps.project.domain.entity.project import Project
from src.apps.project.domain.types_ids import ProjectId, WorkspaceId
from src.apps.project.dtos import UpdateProjectAppDTO
from src.apps.project.exceptions import (
    ProjectException,
    ProjectNotFound,
    ProjectNotUpdated,
)
from src.apps.project.i_project_repository import IProjectRepository
from src.apps.project.mapper import ProjectMapper


class UpdateProjectUseCase:
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository

    async def execute(
        self, project_id: ProjectId, workspace_id: WorkspaceId, update_data: UpdateProjectAppDTO
    ) -> None:
        existing_project = await self._get_existing_project_in_workspace(project_id, workspace_id)
        updated_project = self._map_to_update_data(existing_project, update_data)
        try:
            await self._project_repository.update(updated_project)
        except ProjectNotUpdated as error:
            raise ProjectException(f'{str(error)}')

    async def _get_existing_project_in_workspace(
        self, project_id: ProjectId, workspace_id: WorkspaceId
    ) -> Project:
        try:
            existing_project = await self._project_repository.find_by_id(project_id, workspace_id)
        except ProjectNotFound as error:
            raise ProjectException(f'{str(error)}')
        else:
            return existing_project

    @staticmethod
    def _map_to_update_data(project: Project, update_data: UpdateProjectAppDTO) -> Project:
        try:
            updated_project = ProjectMapper.update_data(project, update_data)
        except ValueError as error:
            raise ProjectException(f'{str(error)}')
        else:
            return updated_project
