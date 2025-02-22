from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from src.api.dtos.workspace_dtos import (
    CreateWorkspaceRequestDTO,
    MemberResponseDTO,
    ResponseWorkspaceDTO,
    UpdateWorkspaceRequestDTO,
)
from src.apps.workspace.dtos.workspace_dtos import (
    CreateWorkspaceDTO,
    DeleteWorkspaceDTO,
    GetWorkspacesByMemberIdDTO,
    OptionalWorkspaceUpdateFields,
    UpdateWorkspaceDTO,
)
from src.apps.workspace.interactors.workspace_interactors import (
    CreateWorkspaceInteractor,
    DeleteWorkspaceInteractor,
    GetWorkspaceByIdInteractor,
    GetWorkspaceByMemberInteractor,
    GetWorkspaceMembersInteractor,
    UpdateWorkspaceInteractor,
)
from src.providers.context import WorkspaceContext

workspace_router = APIRouter(route_class=DishkaRoute)


@workspace_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
)
async def create_workspace(
    body: CreateWorkspaceRequestDTO, interactor: FromDishka[CreateWorkspaceInteractor]
) -> None:
    create_workspace_data = CreateWorkspaceDTO(**body.model_dump())
    await interactor.execute(create_workspace_data=create_workspace_data)


@workspace_router.get('/members')
async def get_workspace_members(
    interactor: FromDishka[GetWorkspaceMembersInteractor], context: FromDishka[WorkspaceContext]
) -> list[MemberResponseDTO]:
    members = await interactor.execute(workspace_id=context.workspace_id)
    return [MemberResponseDTO.model_validate(member) for member in members]


@workspace_router.get(
    '/{workspace_id}', status_code=status.HTTP_200_OK, response_model=ResponseWorkspaceDTO
)
async def get_workspace_by_id(
    workspace_id: UUID, interactor: FromDishka[GetWorkspaceByIdInteractor]
) -> ResponseWorkspaceDTO:
    workspace = await interactor.execute(workspace_id)
    return ResponseWorkspaceDTO.model_validate(workspace)


@workspace_router.get(
    '/', status_code=status.HTTP_200_OK, response_model=list[ResponseWorkspaceDTO]
)
async def get_workspaces_by_member_id(
    member_id: UUID, interactor: FromDishka[GetWorkspaceByMemberInteractor]
) -> list[ResponseWorkspaceDTO]:
    workspaces = await interactor.execute(GetWorkspacesByMemberIdDTO(member_id=member_id))
    return [ResponseWorkspaceDTO.model_validate(workspace) for workspace in workspaces]


@workspace_router.patch('/{workspace_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_workspace(
    body: UpdateWorkspaceRequestDTO,
    workspace_id: UUID,
    interactor: FromDishka[UpdateWorkspaceInteractor],
) -> None:
    workspace_update_data = UpdateWorkspaceDTO(
        updated_fields=OptionalWorkspaceUpdateFields(**body.model_dump(exclude_unset=True)),
        workspace_id=workspace_id,
    )
    await interactor.execute(workspace_update_data=workspace_update_data)


@workspace_router.delete('/{workspace_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(
    workspace_id: UUID, owner_id: UUID, interactor: FromDishka[DeleteWorkspaceInteractor]
) -> None:
    await interactor.execute(DeleteWorkspaceDTO(workspace_id=workspace_id, owner_id=owner_id))
