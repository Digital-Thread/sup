from abc import ABC, abstractmethod

from ..domain.meet import ParticipantEntity
from ..domain.type_ids import (
    MeetId,
    ParticipantId,
    WorkspaceId,
)


class IParticipantRepository(ABC):
    @abstractmethod
    async def add_participant(self, participant: ParticipantEntity) -> ParticipantId:
        raise NotImplementedError

    @abstractmethod
    async def get_participant_by_id(
        self, participant_id: ParticipantId
    ) -> ParticipantEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_participants_by_meet_id(
        self, workspace_id: WorkspaceId, meet_id: MeetId
    ) -> list[ParticipantEntity]:
        raise NotImplementedError

    @abstractmethod
    async def add_bulk(self, participants: list[ParticipantEntity]) -> list[ParticipantId]:
        raise NotImplementedError

    @abstractmethod
    async def update_participant(self, participant: ParticipantEntity) -> ParticipantId:
        raise NotImplementedError

    @abstractmethod
    async def delete_participant(self, participant_id: ParticipantId) -> None:
        raise NotImplementedError
