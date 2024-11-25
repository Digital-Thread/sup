from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Literal, NamedTuple, TypedDict

from src.apps.feature.domain import (
    FeatureEntity,
    FeatureId,
    ProjectId,
    Status,
    TagId,
    UserId,
    WorkspaceId,
)


class OrderByField(Enum):
    NAME = 'name'
    ASSIGNED_TO = 'assigned_to_id'
    CREATED_AT = 'created_at'
    PRIORITY = 'priority'
    PROJECT = 'project_id'
    STATUS = 'status'


class SortOrder(Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class OrderBy(NamedTuple):
    field: OrderByField
    order: SortOrder


class FilterField(TypedDict, total=False):
    members: list[UserId]
    tags: list[TagId]
    status: list[Status]
    project: list[ProjectId]


class PaginateParams(NamedTuple):
    offset: int
    limit_by: Literal[5, 10, None]


@dataclass
class FeatureListQuery:
    filters: FilterField | None = None
    order_by: OrderBy | None = OrderBy(OrderByField.PRIORITY, SortOrder.DESC)
    paginate_by: PaginateParams = PaginateParams(offset=0, limit_by=10)


class IFeatureRepository(ABC):

    @abstractmethod
    async def save(self, feature: FeatureEntity) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, feature_id: FeatureId) -> FeatureEntity | None:
        pass

    @abstractmethod
    async def update(self, feature_id: FeatureId, feature: FeatureEntity) -> None:
        pass

    @abstractmethod
    async def delete(self, feature_id: FeatureId) -> None:
        pass

    @abstractmethod
    async def get_list(
        self, workspace_id: WorkspaceId, query: FeatureListQuery
    ) -> list[tuple[FeatureId, FeatureEntity]]:
        pass
