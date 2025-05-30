from abc import ABC, abstractmethod
from uuid import UUID

from src.apps.project.domain.project import ProjectEntity
from src.apps.project.domain.types_ids import ParticipantId, ProjectId, WorkspaceId


class IProjectRepository(ABC):

    @abstractmethod
    async def check_user_in_workspace(self, user_ids: set[UUID], workspace_id: WorkspaceId) -> None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, project: ProjectEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self, project_id: ProjectId, workspace_id: WorkspaceId
    ) -> ProjectEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_workspace_id(
        self, workspace_id: WorkspaceId, page: int, page_size: int
    ) -> list[tuple[ProjectEntity, list[dict[str, str]] | None]]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, project: ProjectEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_participants(
        self,
        project_id: ProjectId,
        update_participants: list[ParticipantId],
        workspace_id: WorkspaceId,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, project_id: ProjectId, workspace_id: WorkspaceId) -> None:
        raise NotImplementedError
