from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Path, status, Query

from src.api.dtos.role import (
    CreateRoleDTO,
    RoleResponseDTO,
    RoleWithMembersResponseDTO,
    UpdateRoleDTO,
)
from src.apps.workspace.dtos.role_dtos import (
    AssignRoleToWorkspaceMemberDTO,
    CreateRoleAppDTO,
    UpdateRoleAppDTO, GetRolesDTO,
)
from src.apps.workspace.interactors.role_interactors import (
    AssignRoleToWorkspaceMemberInteractor,
    CreateRoleInteractor,
    DeleteRoleInteractor,
    GetRoleByIdInteractor,
    GetRolesByWorkspaceInteractor,
    UpdateRoleInteractor,
)
from src.apps.workspace.interactors.role_interactors.remove_role_from_workspace_member import (
    RemoveRoleFromWorkspaceMemberInteractor,
)
from src.providers.context import WorkspaceContext

role_router = APIRouter(route_class=DishkaRoute)


@role_router.post('', status_code=status.HTTP_201_CREATED)
async def create_role(
    body: CreateRoleDTO,
    interactor: FromDishka[CreateRoleInteractor],
    context: FromDishka[WorkspaceContext],
) -> None:
    create_role_data = CreateRoleAppDTO(**body.model_dump(), workspace_id=context.workspace_id)
    await interactor.execute(create_role_data)


@role_router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[RoleWithMembersResponseDTO],
    response_model_exclude_none=True,
)
async def get_roles_in_workspace(
    interactor: FromDishka[GetRolesByWorkspaceInteractor],
    context: FromDishka[WorkspaceContext],
    page: int = Query(1, description='Page number', ge=1),
    page_size: int = Query(10, description='Number of roles per page', ge=5, le=100)
) -> list[RoleWithMembersResponseDTO]:
    roles = await interactor.execute(
        request_data=GetRolesDTO(workspace_id=context.workspace_id, page=page, page_size=page_size)
    )
    return [RoleWithMembersResponseDTO.model_validate(role) for role in roles]


@role_router.get('/{role_id}', status_code=status.HTTP_200_OK, response_model=RoleResponseDTO)
async def get_role_by_id(
    role_id: Annotated[int, Path()],
    interactor: FromDishka[GetRoleByIdInteractor],
    context: FromDishka[WorkspaceContext],
) -> RoleResponseDTO:
    role = await interactor.execute(role_id=role_id, workspace_id=context.workspace_id)
    return RoleResponseDTO.model_validate(role)


@role_router.patch('/{role_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_role(
    body: UpdateRoleDTO,
    role_id: int,
    interactor: FromDishka[UpdateRoleInteractor],
    context: FromDishka[WorkspaceContext],
) -> None:
    updated_role_data = UpdateRoleAppDTO(
        **body.model_dump(exclude_none=True), id=role_id, workspace_id=context.workspace_id
    )
    await interactor.execute(updated_role_data=updated_role_data)


@role_router.delete('/{role_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_role_by_id(
    role_id: int,
    interactor: FromDishka[DeleteRoleInteractor],
    context: FromDishka[WorkspaceContext],
) -> None:
    await interactor.execute(role_id=role_id, workspace_id=context.workspace_id)


@role_router.post('/{role_id}', status_code=status.HTTP_204_NO_CONTENT)
async def assign_role_to_workspace_member(
    role_id: int,
    member_id: Annotated[UUID, Body(embed=True)],
    interactor: FromDishka[AssignRoleToWorkspaceMemberInteractor],
    context: FromDishka[WorkspaceContext],
) -> None:
    request = AssignRoleToWorkspaceMemberDTO(
        member_id=member_id, id=role_id, workspace_id=context.workspace_id
    )
    await interactor.execute(request)


@role_router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def remove_role_from_workspace_member(
    member_id: Annotated[UUID, Body(embed=True)],
    interactor: FromDishka[RemoveRoleFromWorkspaceMemberInteractor],
    context: FromDishka[WorkspaceContext],
) -> None:
    await interactor.execute(member_id=member_id, workspace_id=context.workspace_id)
