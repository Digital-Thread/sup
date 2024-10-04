from .dtos import (
    InvitedMeetDTO,
    MeetInputDTO,
    MeetResponseDTO,
    ParticipantResponseDTO,
    ParticipantUpdateDTO,
)
from .entities.meet import Meet
from .entities.participant import Participant
from .entities.value_objects import MeetId, ParticipantId
from .exceptions import (
    MeetCreateException,
    MeetInviteException,
    MeetNotFoundException,
    ParticipantCheckException,
    ParticipantNotFoundException,
)
from .repositories import IMeetRepository, IParticipantRepository, MeetListQuery


class MeetService:
    def __init__(
        self,
        meet_repository: IMeetRepository,
        participant_repository: IParticipantRepository,
    ):
        self.meet_repository = meet_repository
        self.participant_repository = participant_repository

    async def create_meet(self, dto: MeetInputDTO) -> MeetId:
        try:
            meet = Meet(**dto.__dict__)
        except ValueError as e:
            raise MeetCreateException() from e
        return await self.meet_repository.create_meet(meet)

    async def get_meets(self, query: MeetListQuery) -> list[MeetResponseDTO]:
        meets = await self.meet_repository.get_meets(query)
        if not meets:
            raise MeetNotFoundException()
        return [MeetResponseDTO(**m.__dict__) for m in meets]

    async def get_meet_by_id(self, meet_id: MeetId) -> MeetResponseDTO:
        meet = await self.meet_repository.get_meet_by_id(meet_id)
        if not meet:
            raise MeetNotFoundException()
        return MeetResponseDTO(**meet.__dict__)

    async def invite(self, dto: InvitedMeetDTO):
        try:
            participant = Participant(**dto.__dict__)
        except ValueError as e:
            raise MeetInviteException() from e

        await self.participant_repository.invite(participant)

    async def get_participants(self, meet_id: MeetId) -> list[ParticipantResponseDTO]:
        participants = await self.participant_repository.get_participants_by_meet_id(meet_id)
        if not participants:
            raise ParticipantNotFoundException()
        return [ParticipantResponseDTO(**p.__dict__) for p in participants]

    async def update_participant(self, dto: ParticipantUpdateDTO) -> ParticipantId:
        try:
            participant = Participant(**dto.__dict__)
        except ValueError as e:
            raise ParticipantCheckException() from e

        return await self.participant_repository.update_participant(participant)
