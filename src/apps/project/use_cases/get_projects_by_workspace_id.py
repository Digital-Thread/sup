from uuid import UUID

from src.apps.project.domain.types_ids import WorkspaceId
from src.apps.project.dtos import ProjectWithParticipantCountAppDTO
from src.apps.project.exceptions import ProjectException, WorkspaceForProjectNotFound
from src.apps.project.i_project_repository import IProjectRepository
from src.apps.project.mapper import ProjectMapper


class GetProjectByWorkspaceUseCase:
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository

    async def execute(self, workspace_id: UUID) -> list[ProjectWithParticipantCountAppDTO]:
        try:
            projects = await self._project_repository.find_by_workspace_id(
                WorkspaceId(workspace_id)
            )
        except WorkspaceForProjectNotFound as error:
            raise ProjectException(f'{str(error)}')
        else:
            return ProjectMapper.list_tuple_to_dto(projects)
