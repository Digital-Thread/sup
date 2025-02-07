from uuid import UUID

from src.apps.project.domain.project import ProjectEntity
from src.apps.project.domain.types_ids import ParticipantId, ProjectId
from src.apps.project.dtos import ProjectUpdateDTO
from src.apps.project.exceptions import (
    ParticipantNotFound,
    ProjectException,
    ProjectNotFound,
    ProjectNotUpdated,
)
from src.apps.project.interactors.update_participants import UpdateParticipantsInteractor
from src.apps.project.project_repository import IProjectRepository
from src.apps.project.mapper import ProjectMapper
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceMemberNotFound


class UpdateProjectInteractor:
    def __init__(self, project_repository: IProjectRepository, update_participants_interactor: UpdateParticipantsInteractor):
        self._project_repository = project_repository
        self._update_participants_interactor = update_participants_interactor

    async def execute(
        self, project_id: int, updated_data: ProjectUpdateDTO
    ) -> None:
        existing_project = await self._get_existing_project_in_workspace(ProjectId(project_id))
        await self._check_user_in_workspace(updated_data.assigned_to, updated_data.participant_ids)
        await self._update_participants_interactor.execute(existing_project, updated_data)
        updated_project = self._apply_update_data_to_project(existing_project, updated_data)

        try:
            await self._project_repository.update(updated_project)
        except ProjectNotUpdated as error:
            raise ProjectException(str(error)) from error

    async def _get_existing_project_in_workspace(
        self, project_id: ProjectId
    ) -> ProjectEntity:
        try:
            existing_project = await self._project_repository.get_by_id(project_id)
        except ProjectNotFound as error:
            raise ProjectException(str(error)) from error
        else:
            return existing_project

    async def _check_user_in_workspace(self, assigned_to: UUID | None, participants_ids: list[UUID] | None) -> None:
        user_ids = ProjectMapper.map_to_set_users(assigned_to, participants_ids)

        if user_ids:
            try:
                await self._project_repository.check_user_in_workspace(user_ids)
            except WorkspaceMemberNotFound as error:
                raise ProjectException(str(error))

    @staticmethod
    def _apply_update_data_to_project(
        project: ProjectEntity, update_data: ProjectUpdateDTO
    ) -> ProjectEntity:
        try:
            updated_project = ProjectMapper.update_data(project, update_data)
        except ValueError as error:
            raise ProjectException(str(error)) from error
        else:
            return updated_project
