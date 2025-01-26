from ..domain import MeetId
from ..dtos import MeetInputDTO
from ..exceptions import (
    MeetCreateError,
    MeetRepositoryError,
)
from ..mappers import MeetMapper
from ..repositories import IMeetRepository
from .base_interactor import BaseInteractor


class CreateMeetInteractor(BaseInteractor):
    def __init__(self, meet_repository: IMeetRepository):
        self._repository = meet_repository

    async def execute(self, dto: MeetInputDTO) -> MeetId:
        try:
            meet = MeetMapper.dto_to_entity(dto)
        except ValueError as e:
            raise MeetCreateError(context=e) from None

        try:
            return await self._repository.save(meet=meet)
        except MeetRepositoryError as e:
            raise MeetCreateError(context=e) from None
