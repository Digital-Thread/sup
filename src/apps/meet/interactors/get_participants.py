from ..domain import MeetId
from ..dtos import ParticipantOutputDTO
from ..mappers import ParticipantMapper
from ..repositories import IParticipantRepository
from .base_interactor import BaseInteractor


class GetListParticipantsInteractor(BaseInteractor):
    def __init__(self, meet_repository: IParticipantRepository):
        self._repository = meet_repository

    async def execute(self, meet_id: MeetId) -> list[ParticipantOutputDTO] | None:
        participants = await self._repository.get_all(meet_id)
        return [ParticipantMapper.entity_to_dto(p) for p in participants] if participants else None
