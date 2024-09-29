from abc import ABC, abstractmethod

from src.apps.meet.entities.meet_dtos import AddMeetDTO, MeetDTO
from src.apps.meet.entities.participant_dtos import (
    InvitedMeetDTO,
    ParticipantMeetDTO,
    UpdateStatusParticipantMeetDTO,
)


class IMeetRepository(ABC):
    @abstractmethod
    async def get_meets(self, **filter_by: str | int) -> list[MeetDTO]:
        raise NotImplementedError

    @abstractmethod
    async def get_meet_by_id(self, id_: int) -> MeetDTO:
        raise NotImplementedError

    @abstractmethod
    async def add_meet(self, dto: AddMeetDTO) -> None:
        raise NotImplementedError


class IParticipantRepository(ABC):
    @abstractmethod
    async def get_participants_by_meet_id(self, meet_id: int) -> list[ParticipantMeetDTO]:
        raise NotImplementedError

    @abstractmethod
    async def invite(self, meet_id: int, dto: InvitedMeetDTO) -> None:
        raise NotImplementedError

    @abstractmethod
    async def check_participant(self, meet_id: int, dto: UpdateStatusParticipantMeetDTO) -> None:
        raise NotImplementedError


class IMeetRepositoryFactory(ABC):
    @abstractmethod
    def get_meet_repository(self) -> IMeetRepository:
        pass

    @abstractmethod
    def get_participant_repository(self) -> IParticipantRepository:
        pass
