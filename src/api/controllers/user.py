from typing import Any, Dict, Optional

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query, Request, Response

from src.api.dependencies.auth_helpers import authenticate_and_create_tokens
from src.api.dtos.user import (
    AdminCreateUserDTO,
    AdminPasswordUpdateDTO,
    AuthDTO,
    UserCreateDTO,
    UserPasswordUpdateDTO,
    UserResponseDTO,
    UserUpdateDTO,
)
from src.apps.auth import JWTService
from src.apps.user.services import (
    AuthenticateUserService,
    AuthorizeUserService,
    CreateUserService,
    GetUserService,
    UpdateUserService,
)
from src.apps.user.services.password_reset_user_service import PasswordResetUserService
from src.apps.user.services.remove_user_service import RemoveUserService

router = APIRouter(route_class=DishkaRoute)


@router.post('/login')
async def login_user(
    request: Request,
    auth_dto: AuthDTO,
    auth_service: FromDishka[AuthenticateUserService],
    jwt_service: FromDishka[JWTService],
) -> dict[str, str]:
    user = await auth_service.authenticate_user(dto=auth_dto)
    user_agent = request.headers.get('User-Agent')
    access_token, max_age_access, refresh_token, max_age_refresh = (
        await jwt_service.creating_tokens(email=user.email, user_agent=user_agent)
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
) -> UserResponseDTO:
    user = await authenticate_and_create_tokens(request, get_user_service)
    user = await authorize_service.get_authorize_user_by_email(user=user, email=email)
    return UserResponseDTO.model_validate(user)


@router.get('/admin/users', response_model=Dict[str, Any])
async def get_users(
    request: Request,
    get_user_service: FromDishka[GetUserService],
    authorize_service: FromDishka[AuthorizeUserService],
    page: Optional[int] = Query(1, ge=1, description='Номер страницы'),
    limit: Optional[int] = Query(50, ge=10, le=50, description='Лимит пользователей на странице'),
    sort_by: Optional[str] = Query(None, description='Поле для сортировки'),
    sort_order: Optional[str] = Query(
        'asc', regex='^(asc|desc)$', description='Порядок сортировки'
    ),
) -> Dict[str, Any]:
    user = await authenticate_and_create_tokens(request, get_user_service)
    await authorize_service.get_authorize_users(user=user)
    offset = (page - 1) * limit
    users = await get_user_service.get_all_users(
        limit=limit, offset=offset, sort_by=sort_by, sort_order=sort_order
    )

    total_users = len(users)


    return {
        'page': page,
        'limit': limit,
        'total_users': total_users,
        'users': [UserResponseDTO.model_validate(user) for user in users],
    }


@router.get('/aboutme', response_model=UserResponseDTO)
async def about_me(
    request: Request,
    get_user_service: FromDishka[GetUserService],
) -> UserResponseDTO:
    user = await authenticate_and_create_tokens(request, get_user_service)
    return UserResponseDTO.model_validate(user)


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


@router.patch('/activate/{activation_token}')
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
    await create_user_service.activate_user_by_admin(user=user)
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
    return {'detail': f'Пользователь зарегистрирован email: {user_email} пароль: {user_password}'}


@router.post('/registration/{invite_token}', response_model=UserResponseDTO)
async def create_user(
    create_user_dto: UserCreateDTO,
    create_user_service: FromDishka[CreateUserService],
    invite_token: str = Path(...),
) -> UserResponseDTO:
    new_user = await create_user_service.create_user(dto=create_user_dto, token=invite_token)
    return UserResponseDTO.model_validate(new_user)


@router.put('/update', response_model=UserResponseDTO)
async def update_user(
    request: Request,
    user_update_dto: UserUpdateDTO,
    update_user_service: FromDishka[UpdateUserService],
    get_user_service: FromDishka[GetUserService],
) -> UserResponseDTO:
    user = await authenticate_and_create_tokens(request, get_user_service)
    user_agent = request.headers.get('User-Agent')

    updated_user = await update_user_service.update_user(
        user=user, user_data=user_update_dto, user_agent=user_agent
    )

    return UserResponseDTO.model_validate(updated_user)


@router.post('/reset_password')
async def reset_password(
    request: Request,
    dto: UserPasswordUpdateDTO,
    get_user_service: FromDishka[GetUserService],
    password_reset_service: FromDishka[PasswordResetUserService],
) -> dict[str, str]:
    user = await authenticate_and_create_tokens(request, get_user_service)
    await password_reset_service.password_reset_user(user.email, dto)

    return {'detail': f'Пароль обновлен'}


@router.post('/admin/reset_password')
async def reset_password_by_admin(
    request: Request,
    dto: AdminPasswordUpdateDTO,
    get_user_service: FromDishka[GetUserService],
    password_reset_service: FromDishka[PasswordResetUserService],
    authorize_service: FromDishka[AuthorizeUserService],
    email: str = Query(...),
) -> dict[str, str]:
    user = await authenticate_and_create_tokens(request, get_user_service)
    await authorize_service.get_access_admin(user)
    await password_reset_service.password_reset_user_by_admin(email, dto)

    return {'detail': f'Пароль обновлен'}


@router.delete('/remove')
async def remove_user(
    request: Request,
    get_user_service: FromDishka[GetUserService],
    remove_user_service: FromDishka[RemoveUserService],
) -> dict[str, str]:
    user = await authenticate_and_create_tokens(request, get_user_service)
    await remove_user_service.remove_user(email=user.email)
    return {'detail': f'Пользователь с email:{user.email} - удален'}


@router.delete('/admin/remove')
async def remove_user_by_admin(
    request: Request,
    get_user_service: FromDishka[GetUserService],
    remove_user_service: FromDishka[RemoveUserService],
    authorize_service: FromDishka[AuthorizeUserService],
    email: str = Query(...),
) -> dict[str, str]:
    user = await authenticate_and_create_tokens(request, get_user_service)
    await authorize_service.get_access_admin(user)
    await remove_user_service.remove_user(email=email)
    return {'detail': f'Пользователь с email:{email} - удален'}
