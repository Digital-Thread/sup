from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, HTTPException, status, Path, Query

from src.api.dtos.role import (
    CreateRoleDTO,
    RoleWithUserCountResponseDTO,
    UpdateRoleDTO, RoleResponseDTO,
)
from src.apps.workspace.dtos.role_dtos import (
    AssignRoleToWorkspaceMemberDTO,
    CreateRoleAppDTO,
    DeleteRoleAppDTO,
    GetRolesAppDTO,
    RemoveRoleFromWorkspaceMemberDTO,
    UpdateRoleAppDTO,
)
from src.apps.workspace.exceptions.role_exceptions import RoleException
from src.apps.workspace.interactors.role_interactors import (
    AssignRoleToWorkspaceMemberInteractor,
    CreateRoleInteractor,
    DeleteRoleInteractor,
    GetRoleByWorkspaceInteractor,
    UpdateRoleInteractor, GetRoleByIdInteractor,
)
from src.apps.workspace.interactors.role_interactors.remove_role_from_workspace_member import (
    RemoveRoleFromWorkspaceMemberInteractor,
)

role_router = APIRouter(route_class=DishkaRoute)


@role_router.post('', status_code=status.HTTP_201_CREATED)
async def create_role(
    body: CreateRoleDTO, interactor: FromDishka[CreateRoleInteractor]
) -> dict[str, str]:
    request = CreateRoleAppDTO(**body.model_dump())
    try:
        await interactor.execute(request)
    except RoleException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return {'redirect_url': '/'}


@role_router.get(
    '/', status_code=status.HTTP_200_OK, response_model=list[RoleWithUserCountResponseDTO]
)
async def get_roles_by_workspace_id(
    workspace_id: UUID, interactor: FromDishka[GetRoleByWorkspaceInteractor]
) -> list[RoleWithUserCountResponseDTO]:
    try:
        response = await interactor.execute(GetRolesAppDTO(workspace_id=workspace_id))
    except RoleException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return [RoleWithUserCountResponseDTO(**role.__dict__) for role in response]


@role_router.get('/{role_id}', status_code=status.HTTP_200_OK, response_model=RoleResponseDTO)
async def get_role_by_id(
        role_id: Annotated[int, Path()],
        workspace_id: Annotated[UUID, Query()],
        interactor: FromDishka[GetRoleByIdInteractor]
) -> RoleResponseDTO:
    try:
        response = await interactor.execute(role_id, workspace_id)
    except RoleException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    else:
        return RoleResponseDTO(**response.__dict__)


@role_router.patch('/{workspace_id}/{role_id}', status_code=status.HTTP_200_OK)
async def update_role(
    body: UpdateRoleDTO,
    workspace_id: UUID,
    role_id: int,
    interactor: FromDishka[UpdateRoleInteractor],
) -> dict[str, str]:
    request = UpdateRoleAppDTO(
        **body.model_dump(exclude_none=True), id=role_id, workspace_id=workspace_id
    )
    try:
        await interactor.execute(request)
    except RoleException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return {'redirect_url': '/'}


@role_router.delete('/{role_id}')
async def delete_role_by_id(
    role_id: int, workspace_id: UUID, interactor: FromDishka[DeleteRoleInteractor]
) -> dict[str, str]:
    try:
        await interactor.execute(DeleteRoleAppDTO(id=role_id, workspace_id=workspace_id))
    except RoleException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return {'redirect_url': '/'}


@role_router.post('/{role_id}', status_code=status.HTTP_204_NO_CONTENT)
async def assign_role_to_workspace_member(
    role_id: int,
    workspace_id: Annotated[UUID, Body()],
    member_id: Annotated[UUID, Body()],
    interactor: FromDishka[AssignRoleToWorkspaceMemberInteractor],
) -> None:
    try:
        await interactor.execute(
            AssignRoleToWorkspaceMemberDTO(
                workspace_id=workspace_id, member_id=member_id, id=role_id
            )
        )
    except RoleException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@role_router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def remove_role_from_workspace_member(
    workspace_id: Annotated[UUID, Body()],
    member_id: Annotated[UUID, Body()],
    interactor: FromDishka[RemoveRoleFromWorkspaceMemberInteractor],
) -> None:
    try:
        await interactor.execute(
            RemoveRoleFromWorkspaceMemberDTO(workspace_id=workspace_id, member_id=member_id)
        )
    except RoleException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
