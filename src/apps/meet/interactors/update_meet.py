from ..dtos import MeetUpdateDTO
from ..exceptions import MeetNotFoundError, MeetRepositoryError, MeetUpdateError
from ..repositories import IMeetRepository
from .base_interactor import BaseInteractor


class UpdateMeetInteractor(BaseInteractor):
    def __init__(self, meet_repository: IMeetRepository, dto: MeetUpdateDTO):
        self._repository = meet_repository
        self._dto = dto

    async def execute(self) -> None:
        meet = await self._repository.get_by_id(self._dto.id)
        if not meet:
            raise MeetNotFoundError()

        try:
            meet.update_fields(self._dto.updated_fields)
        except ValueError as e:
            raise MeetUpdateError(context=e) from e

        try:
            await self._repository.update(meet)
        except MeetRepositoryError as e:
            raise MeetUpdateError(context=e) from e
