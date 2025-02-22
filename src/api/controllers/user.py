from typing import Any, Dict, Optional
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query, Request, Response

from src.api.dependencies.auth_helpers import authenticate_and_create_tokens
from src.api.dtos.user import UserResponseDTO
from src.apps.auth import JWTService
from src.apps.permission import AssignWorkspacePermissionsGroupInteractor
from src.apps.user.dtos import (
    AdminCreateUserDTO,
    AdminPasswordUpdateDTO,
    AuthDTO,
    UserCreateDTO,
    UserPasswordUpdateDTO,
    UserUpdateDTO,
)
from src.apps.user.services import (
    AuthenticateUserService,
    AuthorizeUserService,
    CreateUserService,
    GetUserService,
    UpdateUserService,
)
from src.apps.user.services.password_reset_user_service import PasswordResetUserService
from src.apps.user.services.remove_user_service import RemoveUserService
from src.apps.workspace.domain.entities.workspace_invite import StatusInvite
from src.apps.workspace.dtos.workspace_dtos import CreateWorkspaceDTO
from src.apps.workspace.dtos.workspace_invite_dtos import UpdateWorkspaceInviteAppDTO
from src.apps.workspace.interactors.workspace_interactors import (
    CreateWorkspaceInteractor,
)
from src.apps.workspace.interactors.workspace_interactors.add_member_in_workspace import (
    AddMemberInWorkspaceInteractor,
)
from src.apps.workspace.interactors.workspace_invite_interactors import (
    GetWorkspaceIdByInviteCodeInteractor,
    UpdateWorkspaceInviteInteractor,
)

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
    (
        access_token,
        max_age_access,
        refresh_token,
        max_age_refresh,
    ) = await jwt_service.creating_tokens(email=user.email, user_agent=user_agent)
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
    if isinstance(email, bytes):
        email = email.decode('utf-8')
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


# @router.get('/invite_link')
# async def invite_link(
#     request: Request,
#     get_user_service: FromDishka[GetUserService],
#     create_user_service: FromDishka[CreateUserService],
#     email: str = Query(...),
# ) -> dict[str, str]:
#     user = await authenticate_and_create_tokens(request, get_user_service)

#     await create_user_service.send_invite_link(from_email=user.email, to_email=email)

#     return {'detail': f'Инвайт отправлен на почту {email}'}


@router.patch('/activate/{activation_token}')
async def activate_user(
    create_user_service: FromDishka[CreateUserService],
    activation_token: str = Path(...),
) -> dict[str, str]:
    await create_user_service.activate_user_by_token(token=activation_token)
    return {'detail': 'Ваш аккаунт успешно активирован'}


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
    create_workspace_interactor: FromDishka[CreateWorkspaceInteractor],
) -> dict[str, str]:
    user = await authenticate_and_create_tokens(request, get_user_service)
    await authorize_service.get_access_admin(user)
    user_id, username, user_email, user_password = await create_user_service.create_user_by_admin(
        create_user_dto
    )
    await create_workspace_interactor.execute(CreateWorkspaceDTO(owner_id=user_id, name=username))
    return {'detail': f'Пользователь зарегистрирован email: {user_email} пароль: {user_password}'}


@router.post('/registration/{invite_token}', response_model=UserResponseDTO)
async def create_user_by_invite(
    create_user_dto: UserCreateDTO,
    create_user_service: FromDishka[CreateUserService],
    workspace_invite_interactor: FromDishka[GetWorkspaceIdByInviteCodeInteractor],
    workspace_interactor: FromDishka[CreateWorkspaceInteractor],
    add_member_interactor: FromDishka[AddMemberInWorkspaceInteractor],
    update_status_invite_interactor: FromDishka[UpdateWorkspaceInviteInteractor],
    invite_token: UUID = Path(...),
) -> UserResponseDTO:
    workspace_id, invite_id = await workspace_invite_interactor.execute(invite_token)
    new_user = await create_user_service.create_user(dto=create_user_dto)
    await workspace_interactor.execute(
        CreateWorkspaceDTO(
            name=f'{new_user.first_name} {new_user.last_name}',
            owner_id=new_user.id,
        )
    )
    await add_member_interactor.execute(workspace_id, new_user.id)
    await update_status_invite_interactor.execute(
        UpdateWorkspaceInviteAppDTO(
            id_=invite_id, workspace_id=workspace_id, status=StatusInvite.USED
        ),
    )
    return UserResponseDTO.model_validate(new_user)


@router.post('/registration', response_model=UserResponseDTO)
async def create_user_with_workspace(
    create_user_dto: UserCreateDTO,
    create_user_service: FromDishka[CreateUserService],
    workspace_interactor: FromDishka[CreateWorkspaceInteractor],
    permission_interactor: FromDishka[AssignWorkspacePermissionsGroupInteractor],
) -> UserResponseDTO:
    new_user = await create_user_service.create_user(dto=create_user_dto)
    workspace_id, owner_id = await workspace_interactor.execute(
        CreateWorkspaceDTO(
            name=f'{new_user.first_name} {new_user.last_name}',
            owner_id=new_user.id,
        )
    )
    await permission_interactor.execute(workspace_id=workspace_id, owner_id=owner_id)
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

    return {'detail': 'Пароль обновлен'}


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

    return {'detail': 'Пароль обновлен'}


@router.delete('/remove')
async def remove_user(
    response: Response,
    request: Request,
    get_user_service: FromDishka[GetUserService],
    remove_user_service: FromDishka[RemoveUserService],
    token_service: FromDishka[JWTService],
) -> dict[str, str]:
    user = await authenticate_and_create_tokens(request, get_user_service)
    await remove_user_service.remove_user(email=user.email)
    await token_service.delete_tokens_user(email=user.email)
    response.delete_cookie('sup_access_token')
    response.delete_cookie('sup_refresh_token')
    return {'detail': f'Пользователь с email:{user.email} - удален'}


@router.delete('/admin/remove')
async def remove_user_by_admin(
    request: Request,
    get_user_service: FromDishka[GetUserService],
    remove_user_service: FromDishka[RemoveUserService],
    authorize_service: FromDishka[AuthorizeUserService],
    token_service: FromDishka[JWTService],
    email: str = Query(...),
) -> dict[str, str]:
    user = await authenticate_and_create_tokens(request, get_user_service)
    await authorize_service.get_access_admin(user)
    await token_service.delete_tokens_user(email=email)
    await remove_user_service.remove_user(email=email)
    return {'detail': f'Пользователь с email:{email} - удален'}
