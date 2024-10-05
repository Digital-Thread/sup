from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal, NamedTuple, TypedDict

from .entities.meet import Meet
from .entities.participant import Participant
from .entities.value_objects import (
    AssignedId,
    CategoryId,
    MeetId,
    OwnerId,
    ParticipantId,
    WorkspaceId,
)


class OrderByField(Enum):
    NAME = 'name'
    ASSIGNED_TO = 'assigned_to'
    CREATED_AT = 'created_at'
    MEET_AT = 'meet_at'


class SortOrder(Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class SortBy(NamedTuple):
    field: OrderByField
    order: SortOrder


class MeetFilterFields(TypedDict, total=False):
    category: CategoryId
    assigned_to: AssignedId
    meet_at: datetime


@dataclass
class MeetListQuery:
    filters: MeetFilterFields | None = None
    order_by: SortBy = SortBy(OrderByField.MEET_AT, SortOrder.DESC)
    limit: Literal[5, 10] = 10
    offset: int = 0


class IMeetRepository(ABC):
    @abstractmethod
    async def create_meet(self, owner_id: OwnerId, workspace_id: WorkspaceId, meet: Meet) -> MeetId:
        raise NotImplementedError

    @abstractmethod
    async def get_meets(self, workspace_id: WorkspaceId, query: MeetListQuery) -> list[Meet] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_meet_by_id(self, workspace_id: WorkspaceId, meet_id: MeetId) -> Meet | None:
        raise NotImplementedError

    @abstractmethod
    async def update_meet(self, owner_id: OwnerId, workspace_id: WorkspaceId, meet: Meet) -> Meet:
        raise NotImplementedError


class IParticipantRepository(ABC):
    @abstractmethod
    async def get_participants_by_meet_id(
        self, workspace_id: WorkspaceId, meet_id: MeetId
    ) -> list[Participant] | None:
        raise NotImplementedError

    @abstractmethod
    async def invite(self, workspace_id: WorkspaceId, participant: Participant) -> ParticipantId:
        raise NotImplementedError

    @abstractmethod
    async def update_participant(
        self, workspace_id: WorkspaceId, participant: Participant
    ) -> ParticipantId:
        raise NotImplementedError
