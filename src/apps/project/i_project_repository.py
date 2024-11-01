from abc import ABC, abstractmethod
from uuid import UUID

from src.apps.project.domain.entity.project import Project
from src.apps.project.domain.types_ids import ProjectId, WorkspaceId


class IProjectRepository(ABC):

    @abstractmethod
    async def save(self, project: Project) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, project_id: ProjectId, workspace_id: WorkspaceId) -> Project | None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_workspace_id(self, workspace_id: WorkspaceId) -> list[tuple[Project, int]]:
        raise NotImplementedError

    @abstractmethod
    async def update_project(self, project: Project) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_participants(
        self, project_id: ProjectId, workspace_id: WorkspaceId, update_participants: list[UUID]
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, project_id: ProjectId, workspace_id: WorkspaceId) -> None:
        raise NotImplementedError
