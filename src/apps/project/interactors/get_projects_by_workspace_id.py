from uuid import UUID

from src.apps.project.domain.types_ids import WorkspaceId
from src.apps.project.dtos import PaginationDTO, ProjectWithParticipantsDTO
from src.apps.project.mapper import ProjectMapper
from src.apps.project.project_repository import IProjectRepository


class GetProjectByWorkspaceInteractor:
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository

    async def execute(
            self,
            workspace_id: UUID,
            pagination_data: PaginationDTO) -> list[ProjectWithParticipantsDTO]:
        projects = await self._project_repository.get_by_workspace_id(
                workspace_id=WorkspaceId(workspace_id),
                page=pagination_data.page,
                page_size=pagination_data.page_size
            )
        projects_with_participants_dto = ProjectMapper.list_tuple_to_dto(projects)
        return projects_with_participants_dto
