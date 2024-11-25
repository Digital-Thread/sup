from uuid import UUID

from src.apps.project.domain.entity.project import Project
from src.apps.project.domain.types_ids import ParticipantId, ProjectId, WorkspaceId
from src.apps.project.dtos import UpdateProjectAppDTO
from src.apps.project.exceptions import (
    ParticipantNotFound,
    ProjectException,
    ProjectNotFound,
    ProjectNotUpdated,
)
from src.apps.project.i_project_repository import IProjectRepository
from src.apps.project.mapper import ProjectMapper


class UpdateProjectInteractor:
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository

    async def execute(
        self, project_id: int, workspace_id: UUID, update_data: UpdateProjectAppDTO
    ) -> None:
        existing_project = await self._get_existing_project_in_workspace(
            ProjectId(project_id), WorkspaceId(workspace_id)
        )
        await self.update_participant(existing_project, update_data)
        updated_project = self._apply_update_data_to_project(existing_project, update_data)

        try:
            await self._project_repository.update_project(updated_project)
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

    async def update_participant(
        self, existing_project: Project, update_data: UpdateProjectAppDTO
    ) -> None:
        if self._has_participants_changed(existing_project, update_data):
            try:
                await self._project_repository.update_participants(
                    existing_project.id,
                    existing_project.workspace_id,
                    [ParticipantId(participant) for participant in update_data.participant_ids],
                )
            except ParticipantNotFound as error:
                raise ProjectException(f'{str(error)}')

    @staticmethod
    def _has_participants_changed(
        existing_project: Project, update_data: UpdateProjectAppDTO
    ) -> bool:
        if (
            update_data.participant_ids
            and existing_project.participant_ids != update_data.participant_ids
        ):
            return True

        return False

    @staticmethod
    def _apply_update_data_to_project(
        project: Project, update_data: UpdateProjectAppDTO
    ) -> Project:
        try:
            updated_project = ProjectMapper.update_data(project, update_data)
        except ValueError as error:
            raise ProjectException(f'{str(error)}')
        else:
            return updated_project
