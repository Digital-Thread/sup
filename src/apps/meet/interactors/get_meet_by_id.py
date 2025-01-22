from ..domain import MeetId
from ..dtos import MeetOutputDTO
from ..exceptions import MeetNotFoundError
from ..mappers import MeetMapper
from ..repositories import IMeetRepository
from .base_interactor import BaseInteractor


class GetMeetInteractor(BaseInteractor):
    def __init__(self, meet_repository: IMeetRepository, meet_id: MeetId):
        self._repository = meet_repository
        self._meet_id = meet_id

    async def execute(self) -> MeetOutputDTO:
        meet = await self._repository.get_by_id(self._meet_id)
        if not meet:
            raise MeetNotFoundError()

        meet_dto = MeetMapper.entity_to_dto(meet)
        return meet_dto
