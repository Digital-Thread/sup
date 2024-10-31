from src.apps.project.domain.types_ids import ProjectId, WorkspaceId
from src.apps.project.dtos import ProjectAppDTO
from src.apps.project.exceptions import ProjectNotFound
from src.apps.project.i_project_repository import IProjectRepository
from src.apps.project.mapper import ProjectMapper


class GetProjectByIdUseCase:
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository

    async def execute(self, project_id: ProjectId, workspace_id: WorkspaceId) -> ProjectAppDTO:
        try:
            project = await self._project_repository.find_by_id(project_id, workspace_id)
        except ProjectNotFound:
            raise ValueError(f'Проект с id={project_id} не найден')
        else:
            return ProjectMapper.entity_to_dto(project)
