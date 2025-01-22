from ..domain import MeetId
from ..exceptions import MeetDeleteError, MeetRepositoryError
from ..repositories import IMeetRepository
from .base_interactor import BaseInteractor


class DeleteMeetInteractor(BaseInteractor):
    def __init__(self, meet_repository: IMeetRepository, meet_id: MeetId):
        self._repository = meet_repository
        self._meet_id = meet_id

    async def execute(self):
        try:
            await self._repository.delete(self._meet_id)
        except MeetRepositoryError as e:
            raise MeetDeleteError(context=e) from None
