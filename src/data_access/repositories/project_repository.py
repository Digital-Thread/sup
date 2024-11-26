from logging import warning

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from sqlalchemy import delete, exists, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.apps.project.domain.project import ProjectEntity
from src.apps.project.domain.types_ids import ParticipantId, ProjectId, WorkspaceId
from src.apps.project.exceptions import (
    ParticipantNotFound,
    ProjectAlreadyExists,
    ProjectNotFound,
    WorkspaceForProjectNotFound,
)
from src.apps.project.project_repository import IProjectRepository
from src.data_access.mappers.project_mapper import ProjectMapper
from src.data_access.models.project import ProjectModel
from src.data_access.models.project_participants import ProjectParticipantsModel


class ProjectRepository(IProjectRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory
        self._counter = 0

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
                )

            raise WorkspaceForProjectNotFound(
                f'Рабочего пространства с id={project.workspace_id} не существует'
            )

    async def find_by_id(self, project_id: ProjectId, workspace_id: WorkspaceId) -> ProjectEntity | None:
        query = (
            select(ProjectModel)
            .options(selectinload(ProjectModel.participants))
            .filter_by(id=project_id, workspace_id=workspace_id)
        )
        result = await self._session.execute(query)
        try:
            project_model = result.scalar_one()
        except NoResultFound as error:
            warning(error)
            raise ProjectNotFound(
                f'Проект с id={project_id} не найден в указанном рабочем пространстве.'
            )
        else:
            return ProjectMapper.model_to_entity(project_model)

    async def find_by_workspace_id(self, workspace_id: WorkspaceId) -> list[tuple[ProjectEntity, int]]:
        query = (
            select(
                ProjectModel,
                func.count(ProjectParticipantsModel.participant_id).label('participant_count'),
            )
            .outerjoin(
                ProjectParticipantsModel, ProjectModel.id == ProjectParticipantsModel.project_id
            )
            .where(ProjectModel.workspace_id == workspace_id)
            .group_by(ProjectModel.id)
        )

        result = await self._session.execute(query)
        list_projects_with_user_count = result.all()
        projects = ProjectMapper.list_to_entity(list_projects_with_user_count)

        if not projects:
            raise WorkspaceForProjectNotFound(
                f'Рабочее пространство с id={workspace_id} не найдено'
            )

        return projects

    async def delete(self, project_id: ProjectId, workspace_id: WorkspaceId) -> None:
        exists_project = await self._session.execute(
            select(
                exists().where(
                    ProjectModel.id == project_id, ProjectModel.workspace_id == workspace_id
                )
            )
        )

        if not exists_project.scalar():
            raise ProjectNotFound(f'Проект с id={project_id} не найден в рабочем пространстве')

        stmt = delete(ProjectModel).filter_by(id=project_id, workspace_id=workspace_id)
        await self._session.execute(stmt)

    async def update_project(self, project: ProjectEntity) -> None:
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
        workspace_id: WorkspaceId,
        update_participants: list[ParticipantId],
    ) -> None:
        await self._delete_participants(project_id, workspace_id)
        await self._insert_participants(project_id, workspace_id, update_participants)

    async def _delete_participants(self, project_id: ProjectId, workspace_id: WorkspaceId) -> None:
        delete_stmt = delete(ProjectParticipantsModel).where(
            ProjectParticipantsModel.project_id == project_id,
            ProjectParticipantsModel.workspace_id == workspace_id,
        )
        await self._session.execute(delete_stmt)

    async def _insert_participants(
        self, project_id: ProjectId, workspace_id: WorkspaceId, participant_ids: list[ParticipantId]
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
                raise ParticipantNotFound(f'Участник не найден')
