from uuid import UUID

from src.apps.project.domain.project import ProjectEntity
from src.apps.project.domain.types_ids import WorkspaceId
from src.apps.project.dtos import ProjectCreateDTO
from src.apps.project.exceptions import (
    ProjectAlreadyExists,
    ProjectException,
    WorkspaceForProjectNotFound,
)
from src.apps.project.mapper import ProjectMapper
from src.apps.project.project_repository import IProjectRepository
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceMemberNotFound


class CreateProjectInteractor:
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository

    async def execute(self, project_data: ProjectCreateDTO) -> None:
        await self._check_user_in_workspace(
            workspace_id=WorkspaceId(project_data.workspace_id),
            assigned_to=project_data.assigned_to,
            participants_ids=project_data.participant_ids,
        )
        project = self._map_to_entity(project_data)
        try:
            await self._project_repository.save(project)
        except (WorkspaceForProjectNotFound, ProjectAlreadyExists) as error:
            if isinstance(error, WorkspaceForProjectNotFound):
                raise
            raise ProjectException(str(error)) from error

    async def _check_user_in_workspace(
        self,
        assigned_to: UUID | None,
        workspace_id: WorkspaceId,
        participants_ids: list[UUID] | None,
    ) -> None:
        user_ids = ProjectMapper.map_to_set_users(assigned_to, participants_ids)

        if user_ids:
            try:
                await self._project_repository.check_user_in_workspace(user_ids, workspace_id)
            except WorkspaceMemberNotFound as error:
                raise ProjectException(str(error)) from None

    @staticmethod
    def _map_to_entity(project_data: ProjectCreateDTO) -> ProjectEntity:
        try:
            project = ProjectMapper.dto_to_entity(project_data)
        except ValueError as error:
            ProjectException(str(error))

        return project
