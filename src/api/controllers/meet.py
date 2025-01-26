from dataclasses import asdict
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, status

from src.api.dtos.meet import (
    CreateMeetRequestDTO,
    MeetResponseDTO,
    QueryParams,
    UpdateMeetRequestDTO,
)
from src.apps.meet import (
    MeetInputDTO,
    MeetListQuery,
    MeetUpdateDTO,
    OrderBy,
    PaginateParams,
)
from src.apps.meet.domain import MeetId, OptionalMeetUpdateFields, WorkspaceId
from src.apps.meet.interactors import (
    CreateMeetInteractor,
    DeleteMeetInteractor,
    GetListMeetsInteractor,
    GetMeetInteractor,
    UpdateMeetInteractor,
)
from src.providers.context import WorkspaceContext

meet_router = APIRouter(route_class=DishkaRoute)


@meet_router.post('/', status_code=status.HTTP_201_CREATED, response_model=MeetId)
async def create_meet(
    dto: CreateMeetRequestDTO,
    interactor: FromDishka[CreateMeetInteractor],
    context: FromDishka[WorkspaceContext],
) -> MeetId:
    workspace_id = context.workspace_id
    meet_dto = MeetInputDTO(WorkspaceId(workspace_id), **dto.model_dump())
    return await interactor.execute(dto=meet_dto)


@meet_router.get('/', status_code=status.HTTP_200_OK, response_model=list[MeetResponseDTO])
async def get_meets(
    query: Annotated[QueryParams, Query()],
    interactor: FromDishka[GetListMeetsInteractor],
    context: FromDishka[WorkspaceContext],
) -> list[MeetResponseDTO]:
    workspace_id = WorkspaceId(context.workspace_id)
    query_params = MeetListQuery(
        filters=query.filters,
        order_by=OrderBy(field=query.order_by_field, order=query.sort_order),
        paginate_by=PaginateParams(offset=query.offset, limit_by=query.per_page.limit_by),
    )
    meets = await interactor.execute(query=query_params)
    return [MeetResponseDTO(**asdict(meet)) for meet in meets] if meets else []


@meet_router.get('/{meet_id}', status_code=status.HTTP_200_OK, response_model=MeetResponseDTO)
async def get_meet_by_id(
    meet_id: MeetId,
    interactor: FromDishka[GetMeetInteractor],
) -> MeetResponseDTO:
    meet = await interactor.execute(meet_id=meet_id)
    return MeetResponseDTO(**asdict(meet))


@meet_router.patch('/{meet_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_meet(
    meet_id: MeetId,
    dto: UpdateMeetRequestDTO,
    interactor: FromDishka[UpdateMeetInteractor],
) -> None:
    update_data = MeetUpdateDTO(
        id=meet_id,
        updated_fields=OptionalMeetUpdateFields(**dto.model_dump(exclude_unset=True)),
    )
    await interactor.execute(update_data)


@meet_router.delete('/{meet_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_meet(
    meet_id: MeetId,
    interactor: FromDishka[DeleteMeetInteractor],
) -> None:
    await interactor.execute(meet_id=meet_id)
