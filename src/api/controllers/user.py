from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from src.api.dtos.user import UserResponseDTO
from src.apps.user.dtos import UserCreateDTO
from src.apps.user.services import (  # AuthenticateUserService,; GetUserService,; UpdateUserService,
    CreateUserService,
)

router = APIRouter(route_class=DishkaRoute)


@router.post('/user/{user_id}', response_model=UserResponseDTO)
async def create_user(
    create_user_dto: UserCreateDTO, create_user_service: FromDishka[CreateUserService]
) -> UserResponseDTO:
    user = await create_user_service.create_user(create_user_dto)
    return user
