from typing import List, Optional

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query, Request, Response

from src.apps.auth import JWTService
from src.apps.user.dtos import AuthDTO, UserCreateDTO, UserResponseDTO
from src.apps.user.services import (
    AuthenticateUserService,
    CreateUserService,
    GetUserService,
    UpdateUserService,
)
from src.apps.user.services.authorize_user_service import AuthorizeUserService

router = APIRouter(route_class=DishkaRoute)


@router.post('/create/user/{user_id}', response_model=UserResponseDTO)
async def create_user(
        create_user_dto: UserCreateDTO, create_user_service: FromDishka[CreateUserService]
) -> UserResponseDTO:
    user = await create_user_service.create_user(create_user_dto)
    return user


@router.post('/login')
async def login_user(
        request: Request,
        auth_dto: AuthDTO,
        auth_service: FromDishka[AuthenticateUserService],
) -> dict[str, str]:
    user = await auth_service.authenticate_user(email=auth_dto.email, password=auth_dto.password)
    user_agent = request.headers.get('User-Agent')
    access_token, max_age_access, refresh_token, max_age_refresh = (
        await auth_service.token_service.creating_tokens(email=user.email, user_agent=user_agent)
    )
    if access_token and refresh_token:
        request.state.new_access_token = access_token
        request.state.new_refresh_token = refresh_token
        request.state.max_age_access = max_age_access
        request.state.max_age_refresh = max_age_refresh
    return {'detail': 'Successfully login'}


@router.post('/logout')
async def logout_user(
        request: Request,
        response: Response,
        token_service: FromDishka[JWTService],
) -> dict[str, str]:
    user_agent = request.headers.get('User-Agent')
    access_token = request.cookies.get('sup_access_token')
    if access_token:
        email = await token_service.decode_access_token(access_token)
    else:
        refresh_token = request.cookies.get('sup_refresh_token')
        email = await token_service.decode_refresh_token(refresh_token)
    await token_service.removing_tokens(email=email, user_agent=user_agent)
    response.delete_cookie('sup_access_token')
    response.delete_cookie('sup_refresh_token')
    return {'detail': 'Successfully logged out'}


@router.get('/user/', response_model=UserResponseDTO)
async def get_user(
        request: Request,
        get_user_service: FromDishka[GetUserService],
        authorize_service: FromDishka[AuthorizeUserService],
        email: str = Query(...),
) -> Optional[UserResponseDTO]:
    user_agent = request.headers.get('User-Agent')
    access_token = request.cookies.get('sup_access_token')
    refresh_token = request.cookies.get('sup_refresh_token')
    user, new_access_token, max_age_access, new_refresh_token, max_age_refresh = (
        await get_user_service.get_user_info(access_token, refresh_token, user_agent)
    )

    if new_access_token and new_refresh_token:
        request.state.new_access_token = new_access_token
        request.state.new_refresh_token = new_refresh_token
        request.state.max_age_access = max_age_access
        request.state.max_age_refresh = max_age_refresh

    return await authorize_service.get_authorize_user_by_email(user=user, email=email)


@router.get('/users/', response_model=Optional[List[UserResponseDTO]])
async def get_users(
        request: Request,
        get_user_service: FromDishka[GetUserService],
        authorize_service: FromDishka[AuthorizeUserService],
) -> Optional[List[UserResponseDTO]]:
    user_agent = request.headers.get('User-Agent')
    access_token = request.cookies.get('sup_access_token')
    refresh_token = request.cookies.get('sup_refresh_token')
    user, new_access_token, max_age_access, new_refresh_token, max_age_refresh = (
        await get_user_service.get_user_info(access_token, refresh_token, user_agent)
    )
    if new_access_token and new_refresh_token:
        request.state.new_access_token = new_access_token
        request.state.new_refresh_token = new_refresh_token
        request.state.max_age_access = max_age_access
        request.state.max_age_refresh = max_age_refresh
    return await authorize_service.get_authorize_users(user=user)


@router.get('/aboutme', response_model=UserResponseDTO)
async def about_me(
        request: Request,
        user_service: FromDishka[GetUserService],
) -> Optional[UserResponseDTO]:
    user_agent = request.headers.get('User-Agent')
    access_token = request.cookies.get('sup_access_token')
    refresh_token = request.cookies.get('sup_refresh_token')
    user, new_access_token, max_age_access, new_refresh_token, max_age_refresh = (
        await user_service.get_user_info(access_token, refresh_token, user_agent)
    )
    if new_access_token and new_refresh_token:
        request.state.new_access_token = new_access_token
        request.state.new_refresh_token = new_refresh_token
        request.state.max_age_access = max_age_access
        request.state.max_age_refresh = max_age_refresh
    return user
