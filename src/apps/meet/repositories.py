from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, NamedTuple, TypedDict

from .entities.meet import Meet
from .entities.participant import Participant
from .entities.value_objects import (
    AssignedId,
    CategoryId,
    MeetId,
    ParticipantId,
    WorkspaceId,
)


class SortBy(NamedTuple):
    field: Literal['name', 'assigned_to', 'meet_at']
    order: Literal['ASC', 'DESC']


class MeetFilterFields(TypedDict, total=False):
    category: CategoryId
    assigned_to: AssignedId
    meet_at: datetime


@dataclass
class MeetListQuery:
    filters: MeetFilterFields | None = None
    order_by: SortBy = SortBy('meet_at', 'DESC')
    limit: Literal[4, 8, 16, 24] | None = 16
    offset: int = 0


class IMeetRepository(ABC):
    @abstractmethod
    async def create_meet(self, meet: Meet) -> MeetId:
        raise NotImplementedError

    @abstractmethod
    async def get_meets(self, workspace_id: WorkspaceId, query: MeetListQuery) -> list[Meet]:
        raise NotImplementedError

    @abstractmethod
    async def get_meet_by_id(self, workspace_id: WorkspaceId, meet_id: MeetId) -> Meet | None:
        raise NotImplementedError

    @abstractmethod
    async def update_meet(self, meet: Meet) -> MeetId | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_meet(self, meet_id: MeetId) -> None:
        raise NotImplementedError


class IParticipantRepository(ABC):
    @abstractmethod
    async def add_participant(self, participant: Participant) -> ParticipantId:
        raise NotImplementedError

    @abstractmethod
    async def get_participant_by_id(self, participant_id: ParticipantId) -> Participant | None:
        raise NotImplementedError

    @abstractmethod
    async def get_participants_by_meet_id(
        self, workspace_id: WorkspaceId, meet_id: MeetId
    ) -> list[Participant]:
        raise NotImplementedError

    @abstractmethod
    async def add_bulk(self, participants: list[Participant]) -> list[ParticipantId]:
        raise NotImplementedError

    @abstractmethod
    async def update_participant(self, participant: Participant) -> ParticipantId:
        raise NotImplementedError

    @abstractmethod
    async def delete_participant(self, participant_id: ParticipantId) -> None:
        raise NotImplementedError
