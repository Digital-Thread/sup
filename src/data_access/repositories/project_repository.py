from logging import warning
from uuid import UUID

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.apps.project.domain.project import ProjectEntity
from src.apps.project.domain.types_ids import ParticipantId, ProjectId, WorkspaceId
from src.apps.project.exceptions import (
    ParticipantNotFound,
    ProjectAlreadyExists,
    ProjectNotDeleted,
    WorkspaceForProjectNotFound,
)
from src.apps.project.project_repository import IProjectRepository
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceMemberNotFound
from src.data_access.mappers.project_mapper import ProjectMapper
from src.data_access.models import WorkspaceMemberModel
from src.data_access.models.project import ProjectModel
from src.data_access.models.project_participants import ProjectParticipantsModel
from src.data_access.models.user import UserModel


class ProjectRepository(IProjectRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def check_user_in_workspace(self, user_ids: set[UUID], workspace_id: WorkspaceId) -> None:
        query = select(WorkspaceMemberModel.user_id).where(
            WorkspaceMemberModel.workspace_id == workspace_id,
            WorkspaceMemberModel.user_id.in_(user_ids),
        )
        result = await self._session.execute(query)
        valid_user_ids = {row.user_id for row in result}

        invalid_users = user_ids - valid_user_ids

        if invalid_users:
            raise WorkspaceMemberNotFound(
                'Пользователь отсутствует в рабочем пространстве, в котором находится проект'
            )

    async def save(self, project: ProjectEntity) -> None:
        stmt_project = ProjectMapper.entity_to_model(project)
        self._session.add(stmt_project)

        try:
            await self._session.flush()
        except IntegrityError as error:
            warning(error)
            if isinstance(error.orig.__cause__, UniqueViolationError):
                raise ProjectAlreadyExists(
                    'Проект с таким именем в этом рабочем пространстве уже существует.'
                ) from error

            raise WorkspaceForProjectNotFound(
                f'Рабочего пространства с id={project.workspace_id} не существует.'
            ) from error

    async def get_by_id(
        self, project_id: ProjectId, workspace_id: WorkspaceId
    ) -> ProjectEntity | None:
        query = (
            select(ProjectModel)
            .filter(ProjectModel.id == project_id, ProjectModel.workspace_id == workspace_id)
            .options(selectinload(ProjectModel.participants))
        )
        result = await self._session.execute(query)
        project_model = result.scalar_one_or_none()

        return ProjectMapper.model_to_entity(project_model) if project_model else None

    async def get_by_workspace_id(
        self,
        workspace_id: WorkspaceId,
        page: int,
        page_size: int,
    ) -> list[tuple[ProjectEntity, list[dict[str, str]] | None]]:
        projects_query = (
            select(ProjectModel)
            .filter_by(workspace_id=workspace_id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        projects_result = await self._session.execute(projects_query)
        projects = projects_result.scalars().all()

        if not projects:
            return []

        project_ids = [project.id for project in projects]
        particpants_query = (
            select(
                ProjectParticipantsModel.project_id,
                UserModel.id,
                UserModel.first_name,
                UserModel.last_name,
                UserModel.avatar,
            )
            .join(UserModel, ProjectParticipantsModel.participant_id == UserModel.id)
            .filter(ProjectParticipantsModel.project_id.in_(project_ids))
        )
        participants_result = await self._session.execute(particpants_query)
        participants = participants_result.all()
        projects_with_participants = ProjectMapper.list_to_entity(
            participants=participants, projects=projects
        )
        return projects_with_participants

    async def delete(self, project_id: ProjectId, workspace_id: WorkspaceId) -> None:
        stmt = delete(ProjectModel).filter_by(id=project_id, workspace_id=workspace_id)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise ProjectNotDeleted(f'Проект с id={project_id} не удален.')

    async def update(self, project: ProjectEntity) -> None:
        updated_data = ProjectMapper.entity_to_dict(project)
        stmt = (
            update(ProjectModel)
            .where(ProjectModel.id == project.id, ProjectModel.workspace_id == project.workspace_id)
            .values(**updated_data)
        )
        await self._session.execute(stmt)

    async def update_participants(
        self,
        project_id: ProjectId,
        update_participants: list[ParticipantId],
        workspace_id: WorkspaceId,
    ) -> None:
        await self._delete_participants(project_id, workspace_id)
        await self._insert_participants(project_id, update_participants, workspace_id)

    async def _delete_participants(self, project_id: ProjectId, workspace_id: WorkspaceId) -> None:
        delete_stmt = delete(ProjectParticipantsModel).where(
            ProjectParticipantsModel.project_id == project_id,
            ProjectParticipantsModel.workspace_id == workspace_id,
        )
        await self._session.execute(delete_stmt)

    async def _insert_participants(
        self, project_id: ProjectId, participant_ids: list[ParticipantId], workspace_id: WorkspaceId
    ) -> None:
        participant_insert_stmt = insert(ProjectParticipantsModel).values(
            [
                {
                    'project_id': project_id,
                    'workspace_id': workspace_id,
                    'participant_id': participant_id,
                }
                for participant_id in participant_ids
            ]
        )
        participant_insert_stmt = participant_insert_stmt.on_conflict_do_nothing(
            index_elements=['project_id', 'workspace_id', 'participant_id']
        )
        try:
            await self._session.execute(participant_insert_stmt)
        except IntegrityError as error:
            warning(error)
            if isinstance(error.orig.__cause__, ForeignKeyViolationError):
                raise ParticipantNotFound('Участник не найден.') from error
