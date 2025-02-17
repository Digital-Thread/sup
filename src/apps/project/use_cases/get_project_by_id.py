from uuid import UUID

from src.apps.project.domain.project import ProjectEntity
from src.apps.project.domain.types_ids import ParticipantId, ProjectId, WorkspaceId
from src.apps.project.dtos import (
    ProjectWithParticipantsDTO,
)
from src.apps.project.exceptions import ProjectException, ProjectNotFound
from src.apps.project.mapper import ProjectMapper
from src.apps.project.project_repository import IProjectRepository
from src.apps.workspace.dtos.workspace_dtos import MemberOutDTO
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceException
from src.apps.workspace.interactors.workspace_interactors import GetWorkspaceMembersInteractor


class GetProjectByIdUseCase:
    def __init__(
            self,
            project_repository: IProjectRepository,
            workspace_members_interactor: GetWorkspaceMembersInteractor
    ):
        self._project_repository = project_repository
        self._workspace_members_interactor = workspace_members_interactor

    async def execute(self, project_id: int, workspace_id: UUID) -> ProjectWithParticipantsDTO:
        workspace_members = await self.fetch_workspace_members(
            workspace_id=WorkspaceId(workspace_id)
        )
        project = await self._get_existing_project(ProjectId(project_id), WorkspaceId(workspace_id))
        participants = self._map_participants_to_dto(
            workspace_members=workspace_members,
            project_participant_ids=project.participant_ids
        )
        print(ProjectMapper.entity_to_dto(project, participants))
        return ProjectMapper.entity_to_dto(project, participants)

    async def fetch_workspace_members(self, workspace_id: WorkspaceId) -> list[MemberOutDTO]:
        try:
            return await self._workspace_members_interactor.execute(workspace_id=workspace_id)
        except WorkspaceException as error:
            raise ProjectException(
                f'Ошибка при получении участников рабочего пространства: {str(error)}'
            ) from None

    async def _get_existing_project(self, project_id: ProjectId, workspace_id: WorkspaceId) -> ProjectEntity:
        project = await self._project_repository.get_by_id(project_id, workspace_id)

        if not project:
            raise ProjectNotFound(f'Проект с id={project_id} не найден')

        return project

    @staticmethod
    def _map_participants_to_dto(
        workspace_members: list[MemberOutDTO], project_participant_ids: list[ParticipantId]
    ) -> list[dict[str, UUID | str | bool]]:
        return [
            {
                'id': member.id,
                'full_name': member.name,
                'is_project_participant': member.id in project_participant_ids,
            } for member in workspace_members
        ]
