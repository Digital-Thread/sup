from uuid import UUID

from src.apps.project.domain.types_ids import WorkspaceId
from src.apps.project.dtos import ProjectWithParticipantCountDTO
from src.apps.project.exceptions import ProjectException, WorkspaceForProjectNotFound
from src.apps.project.project_repository import IProjectRepository
from src.apps.project.mapper import ProjectMapper


class GetProjectByWorkspaceInteractor:
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository

    async def execute(self) -> list[ProjectWithParticipantCountDTO]:
        try:
            projects = await self._project_repository.get_by_workspace_id()
        except WorkspaceForProjectNotFound as error:
            raise ProjectException(f'{str(error)}')
        else:
            return ProjectMapper.list_tuple_to_dto(projects)
