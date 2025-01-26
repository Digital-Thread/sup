from ..domain import MeetId
from ..dtos import MeetOutputDTO
from ..exceptions import MeetNotFoundError
from ..mappers import MeetMapper
from ..repositories import IMeetRepository
from .base_interactor import BaseInteractor


class GetMeetInteractor(BaseInteractor):
    def __init__(self, meet_repository: IMeetRepository):
        self._repository = meet_repository

    async def execute(self, meet_id: MeetId) -> MeetOutputDTO:
        meet = await self._repository.get_by_id(meet_id)
        if not meet:
            raise MeetNotFoundError()

        meet_dto = MeetMapper.entity_to_dto(meet)
        return meet_dto
