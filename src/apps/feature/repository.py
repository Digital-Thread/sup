from abc import ABC, abstractmethod

from src.apps.feature.domain import FeatureEntity, FeatureId, WorkspaceId
from src.apps.feature.dtos import (
    FeatureAttrsWithWorkspace,
    FeatureInWorkspaceOutputDTO,
    FeatureOutputDTO,
)
from src.apps.feature.query_parameters import FeatureListQuery


class IFeatureRepository(ABC):

    @abstractmethod
    async def save(self, feature: FeatureEntity) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, feature_id: FeatureId) -> FeatureOutputDTO | None:
        pass

    @abstractmethod
    async def get_entity(self, feature_id: FeatureId) -> FeatureEntity | None:
        pass

    @abstractmethod
    async def update(self, feature: FeatureEntity) -> None:
        pass

    @abstractmethod
    async def delete(self, feature_id: FeatureId) -> None:
        pass

    @abstractmethod
    async def get_by_workspace_id(
        self, workspace_id: WorkspaceId, query: FeatureListQuery
    ) -> list[FeatureInWorkspaceOutputDTO]:
        pass

    @abstractmethod
    async def validate_workspace_consistency(
        self,
        attrs: FeatureAttrsWithWorkspace,
    ) -> None:
        pass
