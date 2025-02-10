from uuid import UUID

from src.apps.project.domain.project import ProjectEntity
from src.apps.project.domain.types_ids import ProjectId, WorkspaceId
from src.apps.project.dtos import ProjectUpdateDTO
from src.apps.project.exceptions import (
    ProjectException,
    ProjectNotFound,
    ProjectNotUpdated,
)
from src.apps.project.interactors.update_participants import UpdateParticipantsInteractor
from src.apps.project.mapper import ProjectMapper
from src.apps.project.project_repository import IProjectRepository
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceMemberNotFound


class UpdateProjectInteractor:
    def __init__(
            self,
            project_repository: IProjectRepository,
            update_participants_interactor: UpdateParticipantsInteractor
        ):
        self._project_repository = project_repository
        self._update_participants_interactor = update_participants_interactor

    async def execute(self, updated_data: ProjectUpdateDTO) -> None:
        existing_project = await self._get_existing_project_in_workspace(
            ProjectId(updated_data.project_id),
            WorkspaceId(updated_data.workspace_id),
        )
        await self._check_user_in_workspace(
            assigned_to=updated_data.assigned_to,
            participants_ids=updated_data.participant_ids,
            workspace_id=WorkspaceId(updated_data.workspace_id)
        )
        await self._update_participants_interactor.execute(existing_project, updated_data)
        updated_project = self._apply_update_data_to_project(existing_project, updated_data)

        try:
            await self._project_repository.update(updated_project)
        except ProjectNotUpdated as error:
            raise ProjectException(str(error)) from error

    async def _get_existing_project_in_workspace(
        self, project_id: ProjectId, workspace_id: WorkspaceId
    ) -> ProjectEntity:
        existing_project = await self._project_repository.get_by_id(
            project_id,
            workspace_id=workspace_id
        )

        if not existing_project:
            raise ProjectNotFound(f'Проект с id={project_id} не найден')

        return existing_project

    async def _check_user_in_workspace(
            self,
            assigned_to: UUID | None,
            participants_ids: list[UUID] | None,
            workspace_id: WorkspaceId
    ) -> None:
        user_ids = ProjectMapper.map_to_set_users(assigned_to, participants_ids)

        if user_ids:
            try:
                await self._project_repository.check_user_in_workspace(
                    user_ids,
                    workspace_id=workspace_id
                )
            except WorkspaceMemberNotFound as error:
                raise ProjectException(str(error)) from None

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
