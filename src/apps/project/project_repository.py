from abc import ABC, abstractmethod

from src.apps.project.domain.project import ProjectEntity
from src.apps.project.domain.types_ids import ParticipantId, ProjectId, WorkspaceId


class IProjectRepository(ABC):

    @abstractmethod
    async def save(self, project: ProjectEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, project_id: ProjectId) -> ProjectEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_workspace_id(self) -> list[tuple[ProjectEntity, int]]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, project: ProjectEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_participants(
        self,
        project_id: ProjectId,
        update_participants: list[ParticipantId],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, project_id: ProjectId) -> None:
        raise NotImplementedError
