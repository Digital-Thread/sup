from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal, NamedTuple, TypedDict

from .domain.type_ids import (
    AssignedId,
    CategoryId,
)


class OrderByField(Enum):
    NAME = 'name'
    ASSIGNED_TO = 'assigned_to'
    MEET_AT = 'meet_at'


class SortOrder(Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class OrderBy(NamedTuple):
    field: OrderByField
    order: SortOrder


class FilterField(TypedDict, total=False):
    name: str
    category: CategoryId
    assigned_to: AssignedId
    meet_at: datetime


class PaginateParams(NamedTuple):
    offset: int = 0
    limit_by: Literal[4, 8, 16, 24] | None = 16


@dataclass
class MeetListQuery:
    filters: FilterField | None = None
    order_by: OrderBy = OrderBy(OrderByField.MEET_AT, SortOrder.DESC)
    paginate_by: PaginateParams = PaginateParams(offset=0, limit_by=16)
