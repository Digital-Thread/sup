from abc import ABC, abstractmethod

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
    async def find_by_workspace_id(self, workspace_id: WorkspaceId) -> list[Project]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, project: Project) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, project_id: ProjectId, workspace_id: WorkspaceId) -> None:
        raise NotImplementedError
