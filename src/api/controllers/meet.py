from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from src.api.dtos.meet import (
    CreateMeetResponse,
    MeetRequest,
    MeetResponse,
    PaginatedParams,
    PaginatedResponse,
)
from src.apps.meet.dtos import MeetFilterFields, MeetInputDTO, MeetListQueryDTO
from src.apps.meet.service import MeetService

router = APIRouter(route_class=DishkaRoute)


async def get_current_user_id() -> UUID:
    user_id = UUID()
    if not user_id:
        raise Exception('User not found')
    return user_id


async def get_current_workspace_id() -> int:
    workspace_id = int(1)
    if not workspace_id:
        raise Exception('Workspace not found')
    return workspace_id


@router.post('/{workspace_id}/meets', response_model=int)
async def create_meet(
    owner_id: Annotated[UUID, Depends(get_current_user_id)],
    workspace_id: Annotated[int, Depends(get_current_workspace_id)],
    dto: MeetRequest,
    meet_service: FromDishka[MeetService],
):
    meet = MeetInputDTO(**dto.model_dump())
    meet_id = await meet_service.create_meet(owner_id, workspace_id, meet)
    return CreateMeetResponse(id=meet_id)


@router.get('/{workspace_id}/meets', response_model=PaginatedResponse[MeetResponse])
async def get_meets(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    workspace_id: Annotated[int, Depends(get_current_workspace_id)],
    paginated_params: Annotated[PaginatedParams, Depends()],
    filters: MeetFilterFields | None,
    meet_service: FromDishka[MeetService],
) -> PaginatedResponse[MeetResponse]:
    query = MeetListQueryDTO(filters=filters, **paginated_params.__dict__)
    meets = await meet_service.get_meets(user_id, workspace_id, query)
    return PaginatedResponse(count=len(meets), items=meets)


@router.get('/{workspace_id}/meets/{meet_id}', response_model=MeetRequest)
async def get_meet_by_id(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    workspace_id: Annotated[int, Depends(get_current_workspace_id)],
    meet_id: int,
    meet_service: FromDishka[MeetService],
):
    return await meet_service.get_meet_by_id(user_id, workspace_id, meet_id)
