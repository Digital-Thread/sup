from ..domain import ParticipantId
from ..exceptions import MeetRepositoryError, ParticipantDeleteError
from ..repositories import IParticipantRepository
from .base_interactor import BaseInteractor


class DeleteParticipantInteractor(BaseInteractor):
    def __init__(self, participant_repository: IParticipantRepository):
        self._repository = participant_repository

    async def execute(self, participant_id: ParticipantId):
        try:
            await self._repository.delete(participant_id)
        except MeetRepositoryError as e:
            raise ParticipantDeleteError(context=e) from None
