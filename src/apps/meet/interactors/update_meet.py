from ..dtos import MeetUpdateDTO
from ..exceptions import MeetNotFoundError, MeetRepositoryError, MeetUpdateError
from ..repositories import IMeetRepository
from .base_interactor import BaseInteractor


class UpdateMeetInteractor(BaseInteractor):
    def __init__(self, meet_repository: IMeetRepository):
        self._repository = meet_repository

    async def execute(self, dto: MeetUpdateDTO) -> None:
        meet = await self._repository.get_by_id(dto.id)
        if not meet:
            raise MeetNotFoundError()

        try:
            meet.update_fields(dto.updated_fields)
        except ValueError as e:
            raise MeetUpdateError(context=e) from e

        try:
            await self._repository.update(meet)
        except MeetRepositoryError as e:
            raise MeetUpdateError(context=e) from e
