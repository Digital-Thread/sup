from uuid import UUID

from src.apps.project.dtos import ProjectCreateDTO
from src.apps.project.exceptions import (
    ProjectAlreadyExists,
    ProjectException,
    WorkspaceForProjectNotFound,
)
from src.apps.project.project_repository import IProjectRepository
from src.apps.project.mapper import ProjectMapper
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceMemberNotFound


class CreateProjectInteractor:
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository

    async def execute(self, project_data: ProjectCreateDTO) -> None:
        await self._check_user_in_workspace(project_data.assigned_to, project_data.participant_ids)

        try:
            await self._project_repository.save(ProjectMapper.dto_to_entity(project_data))
        except (ValueError, WorkspaceForProjectNotFound, ProjectAlreadyExists) as error:
            raise ProjectException(str(error)) from error

    async def _check_user_in_workspace(self, assigned_to: UUID | None, participants_ids: list[UUID] | None) -> None:
        user_ids = ProjectMapper.map_to_set_users(assigned_to, participants_ids)

        if user_ids:
            try:
                await self._project_repository.check_user_in_workspace(user_ids)
            except WorkspaceMemberNotFound as error:
                raise ProjectException(str(error))