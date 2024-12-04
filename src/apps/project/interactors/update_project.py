from src.apps.project.domain.project import ProjectEntity
from src.apps.project.domain.types_ids import ParticipantId, ProjectId
from src.apps.project.dtos import ProjectUpdateDTO
from src.apps.project.exceptions import (
    ParticipantNotFound,
    ProjectException,
    ProjectNotFound,
    ProjectNotUpdated,
)
from src.apps.project.project_repository import IProjectRepository
from src.apps.project.mapper import ProjectMapper


class UpdateProjectInteractor:
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository

    async def execute(
        self, project_id: int, updated_data: ProjectUpdateDTO
    ) -> None:
        existing_project = await self._get_existing_project_in_workspace(ProjectId(project_id))
        await self.update_participant(existing_project, updated_data)
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

    async def update_participant(
        self, existing_project: ProjectEntity, update_data: ProjectUpdateDTO
    ) -> None:
        if self._has_participants_changed(existing_project, update_data):
            try:
                await self._project_repository.update_participants(
                    existing_project.id,
                    [ParticipantId(participant) for participant in update_data.participant_ids],
                )
            except ParticipantNotFound as error:
                raise ProjectException(str(error)) from error

    @staticmethod
    def _has_participants_changed(
        existing_project: ProjectEntity, update_data: ProjectUpdateDTO
    ) -> bool:
        if (
            update_data.participant_ids
            and existing_project.participant_ids != update_data.participant_ids
        ):
            return True

        return False

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
