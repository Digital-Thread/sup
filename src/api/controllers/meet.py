from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.api.dtos.meet import (
    MeetFilterFieldsRequest,
    MeetRequest,
    MeetResponse,
    MeetSortFieldsRequest,
    PaginatedParams,
    PaginatedResponse,
)
from src.apps.meet.dtos import (
    MeetCreateDTO,
    MeetFilterFields,
    MeetListQueryDTO,
    ParticipantCreateDTO,
    SortBy,
)
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


@router.post('/{workspace_id}/meets')
async def create_meet(
    owner_id: Annotated[UUID, Depends(get_current_user_id)],
    workspace_id: Annotated[int, Depends(get_current_workspace_id)],
    dto: MeetRequest,
    meet_service: FromDishka[MeetService],
):
    meet = MeetCreateDTO(
        name=dto.name,
        meet_at=dto.meet_at,
        category_id=dto.category_id,
        assigned_to=dto.assigned_to,
        participants=[ParticipantCreateDTO(**p.model_dump()) for p in dto.participants],
    )
    await meet_service.create_meet(owner_id, workspace_id, meet)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'success': True})


@router.get('/{workspace_id}/meets', response_model=PaginatedResponse[MeetResponse])
async def get_meets(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    workspace_id: Annotated[int, Depends(get_current_workspace_id)],
    paginated_params: Annotated[PaginatedParams, Depends()],
    filters: Annotated[MeetFilterFieldsRequest, Depends()],
    sort_by: Annotated[MeetSortFieldsRequest, Depends()],
    meet_service: FromDishka[MeetService],
) -> PaginatedResponse[MeetResponse]:
    query = MeetListQueryDTO(
        offset=paginated_params.offset if paginated_params else 0,
        limit=paginated_params.limit if paginated_params else None,
        filters=MeetFilterFields(**filters.model_dump(exclude_none=True)),
        order_by=SortBy(sort_by.field, sort_by.order),
    )
    meets = await meet_service.get_meets(user_id, workspace_id, query)
    meets = [MeetResponse.from_dto(meet) for meet in meets]
    return PaginatedResponse(count=len(meets), items=meets)


@router.get('/{workspace_id}/meets/{meet_id}', response_model=MeetResponse)
async def get_meet_by_id(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    workspace_id: Annotated[int, Depends(get_current_workspace_id)],
    meet_id: int,
    meet_service: FromDishka[MeetService],
):
    return await meet_service.get_meet_by_id(user_id, workspace_id, meet_id)
