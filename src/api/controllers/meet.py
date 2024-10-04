from typing import Annotated, Literal

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Query

from src.api.dtos.meet import MeetRequest, MeetResponse, PaginatedResponse
from src.apps.meet.dtos import MeetFilterFields, MeetInputDTO, MeetListQueryDTO
from src.apps.meet.service import MeetService

router = APIRouter(route_class=DishkaRoute)


class PaginatedParams:
    def __init__(
        self,
        page: Annotated[int, Query(default=1)],
        per_page: Annotated[Literal[5, 10], Query(default=10)] = 10,
    ):
        self.limit: Literal[5, 10] = per_page
        self.offset = (page - 1) * per_page


@router.post('/{workspace_id}/meets', response_model=int)
async def create_meet(workspace_id: int, dto: MeetRequest, meet_service: FromDishka[MeetService]):
    meet = MeetInputDTO(workspace_id=workspace_id, **dto.model_dump())
    return await meet_service.create_meet(meet)


@router.get('/{workspace_id}/meets', response_model=PaginatedResponse[MeetResponse])
async def get_meets(
    workspace_id: int,
    paginated_params: Annotated[PaginatedParams, Depends()],
    filters: Annotated[MeetFilterFields | None, Query(default=None)],
    meet_service: FromDishka[MeetService],
) -> PaginatedResponse[MeetResponse]:
    query = MeetListQueryDTO(filters=filters, **paginated_params.__dict__)
    meets = await meet_service.get_meets(workspace_id, query)
    return PaginatedResponse(count=len(meets), items=meets)


@router.get('/{workspace_id}/meets/{id_}', response_model=MeetRequest)
async def get_meet_by_id(workspace_id: int, meet_id: int, meet_service: FromDishka[MeetService]):
    return await meet_service.get_meet_by_id(workspace_id, meet_id)
