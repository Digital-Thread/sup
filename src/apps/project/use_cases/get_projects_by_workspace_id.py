from src.apps.project.domain.types_ids import WorkspaceId
from src.apps.project.dtos import ProjectAppDTO
from src.apps.project.exceptions import ProjectException, WorkspaceForProjectNotFound
from src.apps.project.i_project_repository import IProjectRepository
from src.apps.project.mapper import ProjectMapper


class GetProjectByWorkspaceUseCase:
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository

    async def execute(self, workspace_id: WorkspaceId) -> list[ProjectAppDTO]:
        try:
            projects = await self._project_repository.find_by_workspace_id(workspace_id)
        except WorkspaceForProjectNotFound as error:
            raise ProjectException(f'{str(error)}')
        else:
            return [ProjectMapper.entity_to_dto(project) for project in projects]