from logging import warning

from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import delete, exists, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.project.domain.entity.project import Project
from src.apps.project.domain.types_ids import ProjectId, WorkspaceId
from src.apps.project.exceptions import (
    ProjectAlreadyExists,
    ProjectNotFound,
    ProjectNotUpdated,
    WorkspaceForProjectNotFound,
)
from src.apps.project.i_project_repository import IProjectRepository
from src.data_access.converters.project_converter import ProjectConverter
from src.data_access.models.project import ProjectModel


class ProjectRepository(IProjectRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def save(self, project: Project) -> None:
        stmt = ProjectConverter.entity_to_model(project)
        self._session.add(stmt)

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

    async def find_by_id(self, project_id: ProjectId, workspace_id: WorkspaceId) -> Project | None:
        query = select(ProjectModel).filter_by(id=project_id, workspace_id=workspace_id)
        result = await self._session.execute(query)
        try:
            project_model = result.scalar_one()
        except NoResultFound as error:
            warning(error)
            raise ProjectNotFound(
                f'Проект с id={project_id} не найден в указанном рабочем пространстве.'
            )
        else:
            return ProjectConverter.model_to_entity(project_model)

    async def find_by_workspace_id(self, workspace_id: WorkspaceId) -> list[Project]:
        query = select(ProjectModel).filter_by(workspace_id=workspace_id)
        result = await self._session.execute(query)
        projects = [ProjectConverter.model_to_entity(project) for project in result.scalars().all()]
        if not projects:
            raise WorkspaceForProjectNotFound(
                f'Рабочее пространство с id={workspace_id} не найдено'
            )

        return projects

    async def update(self, project: Project) -> None:
        update_data = ProjectConverter.entity_to_dict(project)
        stmt = update(ProjectModel).filter_by(id=project.id).values(**update_data)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise ProjectNotUpdated(f'Проект с id={project.id} не обновлена')

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
