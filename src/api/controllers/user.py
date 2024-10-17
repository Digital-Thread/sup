from typing import List, Optional

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query, Request, Response

from src.api.dependencies.auth_helpers import authenticate_and_create_tokens
from src.apps.auth import JWTService
from src.apps.user.dtos import (
    AdminCreateUserDTO,
    AuthDTO,
    UserCreateDTO,
    UserResponseDTO, UserUpdateDTO,
)
from src.apps.user.services import (
    AuthenticateUserService,
    CreateUserService,
    GetUserService,
    UpdateUserService,
)
from src.apps.user.services.authorize_user_service import AuthorizeUserService

router = APIRouter(route_class=DishkaRoute)


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
    return {'detail': 'Успешный вход'}


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
    return {'detail': 'Успешный выход'}


@router.get('/admin/user', response_model=UserResponseDTO)
async def get_user(
    request: Request,
    get_user_service: FromDishka[GetUserService],
    authorize_service: FromDishka[AuthorizeUserService],
    email: str = Query(...),
) -> Optional[UserResponseDTO]:
    user = await authenticate_and_create_tokens(request, get_user_service)
    return await authorize_service.get_authorize_user_by_email(user=user, email=email)


@router.get('/admin/users', response_model=Optional[List[UserResponseDTO]])
async def get_users(
    request: Request,
    get_user_service: FromDishka[GetUserService],
    authorize_service: FromDishka[AuthorizeUserService],
) -> Optional[List[UserResponseDTO]]:
    user = await authenticate_and_create_tokens(request, get_user_service)
    return await authorize_service.get_authorize_users(user=user)


@router.get('/aboutme', response_model=UserResponseDTO)
async def about_me(
    request: Request,
    get_user_service: FromDishka[GetUserService],
) -> Optional[UserResponseDTO]:
    user = await authenticate_and_create_tokens(request, get_user_service)
    return user


@router.get('/invite_link')
async def invite_link(
    request: Request,
    get_user_service: FromDishka[GetUserService],
    authorize_service: FromDishka[AuthorizeUserService],
    create_user_service: FromDishka[CreateUserService],
    email: str = Query(...),
) -> dict[str, str]:
    user = await authenticate_and_create_tokens(request, get_user_service)

    await authorize_service.get_access_admin(user=user)
    await create_user_service.send_invite_link(email=email)

    return {'detail': f'Инвайт отправлен на почту {email}'}


@router.get('/activate/{activation_token}')
async def activate_user(
    create_user_service: FromDishka[CreateUserService],
    activation_token: str = Path(...),
) -> dict[str, str]:
    await create_user_service.activate_user_by_token(token=activation_token)
    return {'detail': f'Ваш аккаунт успешно активирован'}


@router.patch('/admin/activate_user')
async def activate_user_by_admin(
    request: Request,
    get_user_service: FromDishka[GetUserService],
    authorize_service: FromDishka[AuthorizeUserService],
    create_user_service: FromDishka[CreateUserService],
    email: str = Query(...),
) -> dict[str, str]:
    user = await authenticate_and_create_tokens(request, get_user_service)
    await authorize_service.get_access_admin(user)
    await create_user_service.activate_user(email=email)
    return {'detail': f'Пользователь с email:{email} - активирован'}


@router.post('/admin/user_registration')
async def create_user_by_admin(
    request: Request,
    create_user_dto: AdminCreateUserDTO,
    get_user_service: FromDishka[GetUserService],
    authorize_service: FromDishka[AuthorizeUserService],
    create_user_service: FromDishka[CreateUserService],
) -> dict[str, str]:
    user = await authenticate_and_create_tokens(request, get_user_service)
    await authorize_service.get_access_admin(user)
    user_email, user_password = await create_user_service.create_user_by_admin(create_user_dto)
    return {
        'detail': f'Пользователь зарегистрирован email: {user_email} пароль: {user_password}'
    }


@router.post('/user_registration/{invite_token}', response_model=UserResponseDTO)
async def create_user(
    create_user_dto: UserCreateDTO,
    create_user_service: FromDishka[CreateUserService],
    invite_token: str = Path(...),
) -> UserResponseDTO:
    new_user = await create_user_service.create_user(create_user_dto, invite_token)
    return new_user


@router.patch('/update/user', response_model=UserResponseDTO)
async def update_user(
        request: Request,
        user_update_dto: UserUpdateDTO,
        update_user_service: FromDishka[UpdateUserService],
        get_user_service: FromDishka[GetUserService],
) -> UserResponseDTO:
    # Аутентификация и получение текущего пользователя
    user = await authenticate_and_create_tokens(request, get_user_service)

    # Обновление данных пользователя
    updated_user = await update_user_service.update_user(user.email, user_update_dto)

    return updated_user
