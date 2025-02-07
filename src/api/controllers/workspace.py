from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status

from src.api.dtos.workspace_dtos import (
    CreateWorkspaceDTO,
    ResponseWorkspaceDTO,
    UpdateWorkspaceDTO,
)
from src.apps.workspace.dtos.workspace_dtos import (
    CreateWorkspaceAppDTO,
    DeleteWorkspaceAppDTO,
    GetWorkspaceAppDTO,
    GetWorkspacesByMemberIdDTO,
    UpdateWorkspaceAppDTO,
)
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceException
from src.apps.workspace.interactors.workspace_interactors import (
    CreateWorkspaceInteractor,
    DeleteWorkspaceInteractor,
    GetWorkspaceByIdInteractor,
    GetWorkspaceByMemberInteractor,
    UpdateWorkspaceInteractor, GetWorkspaceMembersInteractor,
)

workspace_router = APIRouter(route_class=DishkaRoute)


@workspace_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
)
async def create_workspace(
    body: CreateWorkspaceDTO, interactor: FromDishka[CreateWorkspaceInteractor]
) -> dict[str, str]:
    request = CreateWorkspaceAppDTO(**body.model_dump())
    try:
        await interactor.execute(request)
    except WorkspaceException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    return {'redirect_url': '/'}


@workspace_router.get('/members')
async def get_workspace_members(interactor: FromDishka[GetWorkspaceMembersInteractor]):
    try:
        response = await interactor.execute()
    except WorkspaceException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{str(error)}')

    return response


@workspace_router.get(
    '/{workspace_id}', status_code=status.HTTP_200_OK, response_model=ResponseWorkspaceDTO
)
async def get_workspace_by_id(
    workspace_id: UUID, interactor: FromDishka[GetWorkspaceByIdInteractor]
) -> ResponseWorkspaceDTO:
    try:
        response = await interactor.execute(GetWorkspaceAppDTO(id=workspace_id))
    except WorkspaceException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{str(e)}')

    return ResponseWorkspaceDTO(**response.__dict__)


@workspace_router.get(
    '/', status_code=status.HTTP_200_OK, response_model=list[ResponseWorkspaceDTO]
)
async def get_workspaces_by_member_id(
    member_id: UUID, interactor: FromDishka[GetWorkspaceByMemberInteractor]
) -> list[ResponseWorkspaceDTO]:
    try:
        response = await interactor.execute(GetWorkspacesByMemberIdDTO(member_id=member_id))
    except WorkspaceException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{str(e)}')

    return [ResponseWorkspaceDTO(**workspace.__dict__) for workspace in response]


@workspace_router.patch('/{workspace_id}')
async def update_workspace(
    body: UpdateWorkspaceDTO,
    workspace_id: UUID,
    interactor: FromDishka[UpdateWorkspaceInteractor],
) -> dict[str, str]:
    request = UpdateWorkspaceAppDTO(**body.model_dump(exclude_none=True), id=workspace_id)
    try:
        await interactor.execute(request)
    except WorkspaceException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{str(error)}')

    return {'redirect_url': '/'}


@workspace_router.delete('/{workspace_id}')
async def delete_workspace(
    workspace_id: UUID, owner_id: UUID, interactor: FromDishka[DeleteWorkspaceInteractor]
) -> dict[str, str]:
    try:
        await interactor.execute(DeleteWorkspaceAppDTO(id=workspace_id, owner_id=owner_id))
    except WorkspaceException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{str(error)}')
    return {'redirect_url': '/'}


