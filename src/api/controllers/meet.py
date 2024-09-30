from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from apps.meet.entities.meet_dtos import MeetInputDTO
from apps.meet.service import MeetService
from apps.meet.temp_dtos import UserInputDTO, WorkspaceInputDTO
from src.api.dtos.meet import MeetRequest

router = APIRouter(route_class=DishkaRoute)


@router.get('/{workspace_id}/meets', response_model=list[MeetRequest])
async def get_meets(
    workspace_id: int,
    meet_service: FromDishka[MeetService],
):
    workspace = WorkspaceInputDTO(id=workspace_id)
    owner = UserInputDTO(id=1)
    return await meet_service.get_meets(workspace, owner)


@router.get('/{workspace_id}/meets/{id_}', response_model=MeetRequest)
async def get_meet_by_id(workspace_id: int, id_: int, meet_service: FromDishka[MeetService]):
    workspace = WorkspaceInputDTO(id=workspace_id)
    owner = UserInputDTO(id=1)
    return await meet_service.get_meet_by_id(workspace, owner, id_)


@router.post('/{workspace_id}/meets', response_model=MeetRequest)
async def add_meet(workspace_id: int, dto: MeetRequest, meet_service: FromDishka[MeetService]):
    workspace = WorkspaceInputDTO(id=workspace_id)
    owner = UserInputDTO(id=1)
    meet = MeetInputDTO(**dto.model_dump())
    return await meet_service.add_meet(workspace, owner, meet)
