from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from apps.meet.service import MeetService
from src.api.dtos.meet import MeetRequest

router = APIRouter(route_class=DishkaRoute)


@router.get('/meets', response_model=list[MeetRequest])
async def get_meets(meet_service: FromDishka[MeetService]):
    return await meet_service.get_meets()


@router.get('/meets/{id_}', response_model=MeetRequest)
async def get_meet_by_id(id_: int, meet_service: FromDishka[MeetService]):
    return await meet_service.get_meet_by_id(id_)


@router.post('/meets', response_model=MeetRequest)
async def add_meet(dto: MeetRequest, meet_service: FromDishka[MeetService]):
    return await meet_service.add_meet(dto)
