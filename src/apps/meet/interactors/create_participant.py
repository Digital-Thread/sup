from ..dtos import ParticipantInputDTO
from ..exceptions import MeetRepositoryError, ParticipantCreateError
from ..mappers import ParticipantMapper
from ..repositories import IParticipantRepository
from .base_interactor import BaseInteractor


class CreateParticipantInteractor(BaseInteractor):
    def __init__(self, meet_repository: IParticipantRepository):
        self._repository = meet_repository

    async def execute(self, dto: ParticipantInputDTO) -> None:
        try:
            participant = ParticipantMapper.dto_to_entity(dto)
        except ValueError as e:
            raise ParticipantCreateError(context=e) from None

        try:
            await self._repository.save(participant=participant)
        except MeetRepositoryError as e:
            raise ParticipantCreateError(context=e) from None
