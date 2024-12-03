from uuid import UUID

from src.apps.project.domain.project import ProjectEntity
from src.apps.project.domain.types_ids import ParticipantId, ProjectId
from src.apps.project.dtos import (
    ProjectWithParticipantsDTO,
)
from src.apps.project.exceptions import ProjectException, ProjectNotFound
from src.apps.project.mapper import ProjectMapper
from src.apps.project.project_repository import IProjectRepository
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceException
from src.apps.workspace.interactors.workspace_interactors import GetWorkspaceMembersInteractor


class GetProjectByIdUseCase:
    def __init__(self, project_repository: IProjectRepository, workspace_members_interactor: GetWorkspaceMembersInteractor):
        self._project_repository = project_repository
        self._workspace_members_interactor = workspace_members_interactor

    async def execute(self, project_id: int) -> ProjectWithParticipantsDTO:
        workspace_members = await self.fetch_workspace_members()
        project = await self._get_project(ProjectId(project_id))
        participants = self._map_participants_to_dto(workspace_members, project.participant_ids)

        return ProjectMapper.entity_to_dto(project, participants)

    async def fetch_workspace_members(self) -> dict[UUID, str]:
        try:
            return await self._workspace_members_interactor.execute()
        except WorkspaceException as error:
            raise ProjectException(
                f'Ошибка при получении участников рабочего пространства: {str(error)}'
            )

    async def _get_project(self, project_id: ProjectId) -> ProjectEntity:
        try:
            return await self._project_repository.get_by_id(project_id)
        except ProjectNotFound as error:
            raise ProjectException(f'Проект не найден: {str(error)}')

    @staticmethod
    def _map_participants_to_dto(
        workspace_members: dict[UUID, str], project_participant_ids: list[ParticipantId]
    ) -> list[dict[str, UUID | str | bool]]:
        return [
            {
                'id': member_id,
                'full_name': full_name,
                'is_project_participant': member_id in project_participant_ids,
            } for member_id, full_name in workspace_members.items()
        ]
