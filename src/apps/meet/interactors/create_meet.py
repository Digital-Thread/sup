from ..dtos import MeetInputDTO
from ..exceptions import (
    MeetCreateError,
    MeetRepositoryError,
)
from ..mappers import MeetMapper
from ..repositories import IMeetRepository
from .base_interactor import BaseInteractor


class CreateMeetInteractor(BaseInteractor):
    def __init__(self, meet_repository: IMeetRepository, dto: MeetInputDTO):
        self._repository = meet_repository
        self._dto = dto

    async def execute(self) -> None:
        try:
            meet = MeetMapper.dto_to_entity(self._dto)
        except ValueError as e:
            raise MeetCreateError(context=e) from None

        try:
            await self._repository.save(meet=meet)
        except MeetRepositoryError as e:
            raise MeetCreateError(context=e) from None
