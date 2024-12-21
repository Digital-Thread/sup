from src.apps.project.domain.project import ProjectEntity
from src.apps.project.domain.types_ids import ParticipantId
from src.apps.project.dtos import ProjectUpdateDTO
from src.apps.project.exceptions import ParticipantNotFound, ProjectException
from src.apps.project.project_repository import IProjectRepository


class UpdateParticipantsInteractor:
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository

    async def execute(
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