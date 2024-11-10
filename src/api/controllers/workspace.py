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
    UpdateWorkspaceAppDTO,
)
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceException
from src.apps.workspace.use_cases.workspace_use_cases import (
    CreateWorkspaceUseCase,
    DeleteWorkspaceUseCase,
    GetWorkspaceByIdUseCase,
    GetWorkspaceByMemberUseCase,
    UpdateWorkspaceUseCase,
)

workspace_router = APIRouter(route_class=DishkaRoute)


@workspace_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
)
async def create_workspace(
    body: CreateWorkspaceDTO, use_case: FromDishka[CreateWorkspaceUseCase]
) -> dict[str, str]:
    request = CreateWorkspaceAppDTO(**body.model_dump())
    try:
        await use_case.execute(request)
    except WorkspaceException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    return {'redirect_url': '/'}


@workspace_router.get(
    '/{workspace_id}', status_code=status.HTTP_200_OK, response_model=ResponseWorkspaceDTO
)
async def get_workspace_by_id(
    workspace_id: UUID, use_case: FromDishka[GetWorkspaceByIdUseCase]
) -> ResponseWorkspaceDTO:
    try:
        response = await use_case.execute(workspace_id)
    except WorkspaceException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{str(e)}')

    return ResponseWorkspaceDTO(**response.__dict__)


@workspace_router.get(
    '/', status_code=status.HTTP_200_OK, response_model=list[ResponseWorkspaceDTO]
)
async def get_workspaces_by_member_id(
    member_id: UUID, use_case: FromDishka[GetWorkspaceByMemberUseCase]
) -> list[ResponseWorkspaceDTO]:
    try:
        response = await use_case.execute(member_id)
    except WorkspaceException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{str(e)}')

    return [ResponseWorkspaceDTO(**workspace.__dict__) for workspace in response]


@workspace_router.patch('/{workspace_id}')
async def update_workspace(
    body: UpdateWorkspaceDTO,
    workspace_id: UUID,
    use_case: FromDishka[UpdateWorkspaceUseCase],
) -> dict[str, str]:
    request = UpdateWorkspaceAppDTO(**body.model_dump(exclude_none=True))
    try:
        await use_case.execute(workspace_id, request)
    except WorkspaceException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{str(error)}')

    return {'redirect_url': '/'}


@workspace_router.delete('/{workspace_id}')
async def delete_workspace(
    workspace_id: UUID, owner_id: UUID, use_case: FromDishka[DeleteWorkspaceUseCase]
) -> dict[str, str]:
    try:
        await use_case.execute(workspace_id, owner_id)
    except WorkspaceException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{str(error)}')
    return {'redirect_url': '/'}
