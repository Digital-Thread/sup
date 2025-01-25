from ..domain import ParticipantId
from ..dtos import ParticipantOutputDTO
from ..exceptions import ParticipantNotFoundError
from ..mappers import ParticipantMapper
from ..repositories import IParticipantRepository
from .base_interactor import BaseInteractor


class GetParticipantInteractor(BaseInteractor):
    def __init__(
        self, participant_repository: IParticipantRepository, participant_id: ParticipantId
    ):
        self._repository = participant_repository
        self._participant_id = participant_id

    async def execute(self) -> ParticipantOutputDTO:
        participant = await self._repository.get_by_id(self._participant_id)
        if not participant:
            raise ParticipantNotFoundError()

        participant_dto = ParticipantMapper.entity_to_dto(participant)
        return participant_dto
