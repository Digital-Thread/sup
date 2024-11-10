from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status

from src.api.dtos.meet import (
    MeetFilterFieldsRequest,
    MeetRequestCreate,
    MeetRequestUpdate,
    MeetResponse,
    MeetSortFieldsRequest,
    PaginatedParams,
    PaginatedResponse,
    SuccessResponse,
)
from src.apps.meet.dtos import (
    MeetCreateDTO,
    MeetListQueryDTO,
    MeetUpdateDTO,
    ParticipantCreateDTO,
    ParticipantDeleteDTO,
    ParticipantUpdateDTO,
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


@router.post('', status_code=status.HTTP_201_CREATED, response_model=SuccessResponse)
async def create_meet(
    owner_id: Annotated[UUID, Depends(get_current_user_id)],
    workspace_id: Annotated[int, Depends(get_current_workspace_id)],
    dto: MeetRequestCreate,
    meet_service: FromDishka[MeetService],
) -> SuccessResponse:
    meet = MeetCreateDTO(
        name=dto.name,
        meet_at=dto.meet_at,
        category_id=dto.category_id,
        assigned_to=dto.assigned_to,
        participants=[ParticipantCreateDTO(**p.model_dump()) for p in dto.participants],
    )
    await meet_service.create_meet(owner_id, workspace_id, meet)
    return SuccessResponse(message='Meet created')


@router.get('', response_model=PaginatedResponse[MeetResponse])
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
        filters=filters.to_dto(),
        order_by=SortBy(sort_by.field, sort_by.order),
    )
    meets = await meet_service.get_meets(user_id, workspace_id, query)
    meets_response = [MeetResponse.from_dto(meet) for meet in meets]
    return PaginatedResponse(count=len(meets), items=meets_response)


@router.get('/{meet_id}', response_model=MeetResponse)
async def get_meet_by_id(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    workspace_id: Annotated[int, Depends(get_current_workspace_id)],
    meet_id: int,
    meet_service: FromDishka[MeetService],
) -> MeetResponse:
    meet = await meet_service.get_meet_by_id(user_id, workspace_id, meet_id)
    meet_response = MeetResponse.from_dto(meet)
    return meet_response


@router.patch('/{meet_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_meet(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    workspace_id: Annotated[int, Depends(get_current_workspace_id)],
    meet_id: int,
    meet_request: MeetRequestUpdate,
    meet_service: FromDishka[MeetService],
) -> None:
    dto = MeetUpdateDTO(
        name=meet_request.name,
        meet_at=meet_request.meet_at,
        category_id=meet_request.category_id,
        assigned_to=meet_request.assigned_to,
        participants_to_add=[
            ParticipantCreateDTO(**p.model_dump()) for p in meet_request.participants_to_add
        ],
        participants_to_update=[
            ParticipantUpdateDTO(**p.model_dump()) for p in meet_request.participants_to_update
        ],
        participants_to_delete=[
            ParticipantDeleteDTO(**p.model_dump()) for p in meet_request.participants_to_delete
        ],
    )
    await meet_service.update_meet(user_id, workspace_id, meet_id, dto)


@router.delete('/{meet_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_meet(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    workspace_id: Annotated[int, Depends(get_current_workspace_id)],
    meet_id: int,
    meet_service: FromDishka[MeetService],
) -> None:
    await meet_service.delete_meet(user_id, workspace_id, meet_id)
