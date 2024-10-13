from typing import List, Optional

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query, Request, Response
from fastapi.exceptions import HTTPException

from src.apps.auth import JWTService
from src.apps.user.dtos import AuthDTO, UserCreateDTO, UserResponseDTO
from src.apps.user.services import (
    AuthenticateUserService,
    CreateUserService,
    GetUserService,
    UpdateUserService,
)

router = APIRouter(route_class=DishkaRoute)


@router.post('/create/user/{user_id}', response_model=UserResponseDTO)
async def create_user(
        create_user_dto: UserCreateDTO, create_user_service: FromDishka[CreateUserService]
) -> UserResponseDTO:
    user = await create_user_service.create_user(create_user_dto)
    return user


@router.get('/users/', response_model=List[UserResponseDTO])
async def get_users(
        request: Request,
        user_service: FromDishka[GetUserService],
) -> List[UserResponseDTO]:
    user_agent = request.headers.get('User-Agent')
    access_token = request.cookies.get('sup_access_token')
    refresh_token = request.cookies.get('sup_refresh_token')
    user, _, _, _, _ = await user_service.get_user_info(access_token, refresh_token, user_agent)
    if user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    if user.is_superuser and user.is_active:
        return await user_service.get_all_users()
    else:
        raise HTTPException(status_code=403, detail='У вас нет прав для доступа к этому ресурсу')


@router.post('/login')
async def login_user(
        response: Response,
        request: Request,
        auth_dto: AuthDTO,
        auth_service: FromDishka[AuthenticateUserService],
) -> dict[str, str]:
    user = await auth_service.authenticate_user(email=auth_dto.email, password=auth_dto.password)
    user_agent = request.headers.get('User-Agent')
    access_token, max_age_access, refresh_token, max_age_refresh = (
        await auth_service.token_service.creating_tokens(email=user.email, user_agent=user_agent)
    )
    response.set_cookie(
        'sup_access_token',
        access_token,
        httponly=True,
        max_age=max_age_access,
    )
    response.set_cookie(
        'sup_refresh_token',
        refresh_token,
        httponly=True,
        max_age=max_age_refresh,
    )
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
        decoded_payload = await token_service.decode_token(access_token)
        email = decoded_payload['email']
    else:
        refresh_token = request.cookies.get('sup_refresh_token')
        if not refresh_token:
            raise HTTPException(status_code=401, detail='Вы не в системе')
        decoded_payload = await token_service.decode_token(refresh_token)
        email = decoded_payload['email']
    await token_service.removing_tokens(email=email, user_agent=user_agent)
    response.delete_cookie('sup_access_token')
    response.delete_cookie('sup_refresh_token')
    return {'detail': 'Successfully logged out'}


@router.get('/user/', response_model=UserResponseDTO)
async def get_user(
        request: Request, user_service: FromDishka[GetUserService], email: str = Query(...)
) -> UserResponseDTO:
    user_agent = request.headers.get('User-Agent')
    access_token = request.cookies.get('sup_access_token')
    refresh_token = request.cookies.get('sup_refresh_token')
    user, _, _, _, _ = await user_service.get_user_info(access_token, refresh_token, user_agent)
    if user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    if not user.is_superuser and user.email != email:
        raise HTTPException(status_code=403, detail='Вы можете смотреть информацию только о себе')
    if user.is_superuser and user.is_active:
        return await user_service.get_user_by_email(email)
    if not user.is_superuser and user.email == email:
        return await user_service.get_user_by_email(email)
    raise HTTPException(status_code=403, detail='У вас нет прав для доступа к этому ресурсу')


@router.get('/aboutme', response_model=UserResponseDTO)
async def about_me(
        response: Response,
        request: Request,
        user_service: FromDishka[GetUserService],
) -> Optional[UserResponseDTO]:
    user_agent = request.headers.get('User-Agent')
    access_token = request.cookies.get('sup_access_token')
    refresh_token = request.cookies.get('sup_refresh_token')
    user, new_access_token, max_age_access, new_refresh_token, max_age_refresh = (
        await user_service.get_user_info(access_token, refresh_token, user_agent)
    )
    if user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    if new_access_token and new_refresh_token:
        response.set_cookie(
            'sup_access_token',
            new_access_token,
            httponly=True,
            max_age=max_age_access,
        )
        response.set_cookie(
            'sup_refresh_token',
            new_refresh_token,
            httponly=True,
            max_age=max_age_refresh,
        )
    return user
