from ..domain import ParticipantId
from ..exceptions import MeetRepositoryError, ParticipantDeleteError
from ..repositories import IParticipantRepository
from .base_interactor import BaseInteractor


class DeleteMeetInteractor(BaseInteractor):
    def __init__(
        self, participant_repository: IParticipantRepository, participant_id: ParticipantId
    ):
        self._repository = participant_repository
        self._participant_id = participant_id

    async def execute(self):
        try:
            await self._repository.delete(self._participant_id)
        except MeetRepositoryError as e:
            raise ParticipantDeleteError(context=e) from None
