from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status

from src.api.dtos.meet import ParticipantRequestUpdate
from src.apps.meet.dtos import ParticipantUpdateDTO
from src.apps.meet.service import MeetService

router = APIRouter(route_class=DishkaRoute)


async def get_current_user_id() -> UUID:
    user_id = UUID('973bcf7c-21c2-4c27-85e9-fc38eb826134')
    if not user_id:
        raise Exception('User not found')
    return user_id


async def get_current_workspace_id() -> int:
    workspace_id = int(1)
    if not workspace_id:
        raise Exception('Workspace not found')
    return workspace_id


@router.patch('/{participant_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_participant(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    workspace_id: Annotated[int, Depends(get_current_workspace_id)],
    meet_id: int,
    participant_id: int,
    participant_request: ParticipantRequestUpdate,
    meet_service: FromDishka[MeetService],
) -> None:
    dto = ParticipantUpdateDTO(id=participant_id, status=participant_request.status)
    await meet_service.update_participant(user_id, workspace_id, dto)
