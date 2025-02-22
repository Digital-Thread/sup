from dataclasses import asdict

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from src.api.dtos import CreateGroupRequestDTO, GroupResponseDTO, UpdateGroupRequestDTO
from src.apps.permission import (
    CreatePermissionGroupInteractor,
    PermissionGroupInputDTO,
    GetPermissionGroupsByWorkspaceIdInteractor,
    GetPermissionGroupByIdInteractor,
    UpdatePermissionGroupInteractor,
    PermissionGroupUpdateDTO,
    DeletePermissionGroupInteractor,
)
from src.apps.permission.domain import WorkspaceId, PermissionGroupId, OptionalPermissionGroupUpdateFields
from src.providers.context import WorkspaceContext

perm_group_router = APIRouter(route_class=DishkaRoute)


@perm_group_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_permission_group(
        dto: CreateGroupRequestDTO,
        interactor: FromDishka[CreatePermissionGroupInteractor],
        context: FromDishka[WorkspaceContext],
) -> None:
    workspace_id = context.workspace_id
    perm_group = PermissionGroupInputDTO(WorkspaceId(workspace_id), **dto.model_dump())
    await interactor.execute(dto=perm_group)


@perm_group_router.get('/', status_code=status.HTTP_200_OK, response_model=list[GroupResponseDTO])
async def get_permission_groups_by_workspace_id(
        interactor: FromDishka[GetPermissionGroupsByWorkspaceIdInteractor],
        context: FromDishka[WorkspaceContext],
) -> list[GroupResponseDTO]:
    workspace_id = WorkspaceId(context.workspace_id)
    perm_groups = await interactor.execute(workspace_id=workspace_id)
    return [GroupResponseDTO(**asdict(perm_group)) for perm_group in perm_groups] if perm_groups else []


@perm_group_router.get(
    '/{perm_group_id}', status_code=status.HTTP_200_OK, response_model=GroupResponseDTO
)
async def get_permission_group_by_id(
        perm_group_id: PermissionGroupId,
        interactor: FromDishka[GetPermissionGroupByIdInteractor],
) -> GroupResponseDTO:
    perm_group = await interactor.execute(perm_group_id=perm_group_id)
    return GroupResponseDTO(**asdict(perm_group))


@perm_group_router.patch('/{perm_group_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_permission_group(
        perm_group_id: PermissionGroupId,
        dto: UpdateGroupRequestDTO,
        interactor: FromDishka[UpdatePermissionGroupInteractor],
) -> None:
    update_data = PermissionGroupUpdateDTO(
        id=perm_group_id,
        updated_fields=OptionalPermissionGroupUpdateFields(**dto.model_dump(exclude_unset=True)),
    )
    await interactor.execute(update_data)


@perm_group_router.delete('/{perm_group_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission_group(
        perm_group_id: PermissionGroupId,
        interactor: FromDishka[DeletePermissionGroupInteractor],
) -> None:
    await interactor.execute(perm_group_id=perm_group_id)
