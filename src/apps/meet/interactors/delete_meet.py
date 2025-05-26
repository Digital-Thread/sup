from ..domain import MeetId
from ..exceptions import MeetDeleteError, MeetRepositoryError
from ..repositories import IMeetRepository
from .base_interactor import BaseInteractor


class DeleteMeetInteractor(BaseInteractor):
    def __init__(self, meet_repository: IMeetRepository):
        self._repository = meet_repository

    async def execute(self, meet_id: MeetId) -> None:
        try:
            await self._repository.delete(meet_id)
        except MeetRepositoryError as e:
            raise MeetDeleteError(context=e) from None
