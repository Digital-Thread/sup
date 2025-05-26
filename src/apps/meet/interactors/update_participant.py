from ..dtos import ParticipantUpdateDTO
from ..exceptions import (
    MeetRepositoryError,
    ParticipantNotFoundError,
    ParticipantUpdateError,
)
from ..repositories import IParticipantRepository
from .base_interactor import BaseInteractor


class UpdateParticipantInteractor(BaseInteractor):
    def __init__(self, participant_repository: IParticipantRepository):
        self._repository = participant_repository

    async def execute(self, dto: ParticipantUpdateDTO) -> None:
        participant = await self._repository.get_by_id(dto.id)
        if not participant:
            raise ParticipantNotFoundError()

        try:
            participant.update_fields(dto.updated_fields)
        except ValueError as e:
            raise ParticipantUpdateError(context=e) from e

        try:
            await self._repository.update(participant)
        except MeetRepositoryError as e:
            raise ParticipantUpdateError(context=e) from e
