from apps.meet.entities.meet_dtos import AddMeetDTO, MeetDTO
from apps.meet.entities.participant_dtos import (
    InvitedMeetDTO,
    ParticipantMeetDTO,
    UpdateStatusParticipantMeetDTO,
)

from .exceptions import MeetCreateException, MeetNotFoundException
from .repositories import IMeetRepository, IParticipantRepository


class MeetService:
    def __init__(
        self,
        meet_repository: IMeetRepository,
        participant_repository: IParticipantRepository,
    ):
        self.meet_repository = meet_repository
        self.participant_repository = participant_repository

    async def get_meets(self) -> list[MeetDTO]:
        return await self.meet_repository.get_meets()

    async def get_meet_by_id(self, meet_id: int) -> MeetDTO:
        meet = await self.meet_repository.get_meet_by_id(meet_id)
        if not meet:
            raise MeetNotFoundException()
        return meet

    async def add_meet(self, dto: AddMeetDTO):
        try:
            await self.meet_repository.add_meet(dto)
        except ValueError as e:
            raise MeetCreateException() from e

    async def invite(self, meet_id: int, dtos: list[InvitedMeetDTO]):
        meet = await self.get_meet_by_id(meet_id)
        for dto in dtos:
            await self.participant_repository.invite(dto)

    async def get_participants(self, meet_id: int) -> list[ParticipantMeetDTO]:
        return await self.participant_repository.get_participants_by_meet_id(meet_id)

    async def check_participation(self, dto: UpdateStatusParticipantMeetDTO):
        await self.participant_repository.check_participant(dto)
