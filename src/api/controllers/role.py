from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status

from src.api.dtos.role_dtos import (
    CreateRoleDTO,
    ResponseRoleWithUserCountDTO,
    UpdateRoleDTO,
)
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.dtos.role_dtos import CreateRoleAppDTO, UpdateRoleAppDTO
from src.apps.workspace.exceptions.role_exceptions import RoleException
from src.apps.workspace.use_cases.role_use_cases import (
    CreateRoleUseCase,
    DeleteRoleUseCase,
    GetRoleByWorkspaceUseCase,
    UpdateRoleUseCase,
)

role_router = APIRouter(route_class=DishkaRoute)


@role_router.post('/create_role', status_code=status.HTTP_201_CREATED)
async def create_role(
    body: CreateRoleDTO, use_case: FromDishka[CreateRoleUseCase]
) -> dict[str, str]:
    request = CreateRoleAppDTO(**body.model_dump())  # type: ignore
    try:
        await use_case.execute(request)
    except RoleException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return {'redirect_url': '/'}


@role_router.get(
    '/', status_code=status.HTTP_200_OK, response_model=list[ResponseRoleWithUserCountDTO]
)
async def get_roles_by_workspace_id(
    workspace_id: WorkspaceId, use_case: FromDishka[GetRoleByWorkspaceUseCase]
) -> list[ResponseRoleWithUserCountDTO]:
    try:
        response = await use_case.execute(workspace_id)
    except RoleException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return [ResponseRoleWithUserCountDTO(**role.__dict__) for role in response]


@role_router.patch('/{role_id}', status_code=status.HTTP_200_OK)
async def update_role(
    body: UpdateRoleDTO,
    workspace_id: WorkspaceId,
    role_id: RoleId,
    use_case: FromDishka[UpdateRoleUseCase],
) -> dict[str, str]:
    request = UpdateRoleAppDTO(**body.model_dump(exclude_none=True))  # type: ignore
    try:
        await use_case.execute(role_id, workspace_id, request)
    except RoleException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return {'redirect_url': '/'}


@role_router.delete('/{role_id}')
async def delete_role_by_id(
    role_id: RoleId, workspace_id: WorkspaceId, use_case: FromDishka[DeleteRoleUseCase]
) -> dict[str, str]:
    try:
        await use_case.execute(role_id, workspace_id)
    except RoleException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return {'redirect_url': '/'}
