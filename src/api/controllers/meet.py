from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from src.api.dtos.meet import MeetRequest
from src.apps import IMeetRepository

router = APIRouter(route_class=DishkaRoute)


@router.get('/meets', response_model=list[MeetRequest])
async def get_meets(meet_repo: FromDishka[IMeetRepository]):
    return await meet_repo.get_meets()


@router.get('/meets/{id_}', response_model=MeetRequest)
async def get_meet_by_id(id_: int, meet_repo: FromDishka[IMeetRepository]):
    return await meet_repo.get_meet_by_id(id_)


@router.post('/meets', response_model=MeetRequest)
async def add_meet(dto: MeetRequest, meet_repo: FromDishka[IMeetRepository]):
    return await meet_repo.add_meet(dto)
