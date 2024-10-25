from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, status

from src.api.dtos.workspace_dtos import (
    CreateWorkspaceDTO,
    ResponseWorkspaceDTO,
    UpdateWorkspaceDTO,
)
from src.apps.workspace.domain.types_ids import OwnerId, WorkspaceId
from src.apps.workspace.dtos.workspace_dtos import (
    CreateWorkspaceAppDTO,
    UpdateWorkspaceAppDTO,
)
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceException
from src.apps.workspace.use_cases.workspace_use_cases import (
    CreateWorkspaceUseCase,
    DeleteWorkspaceUseCase,
    GetWorkspaceByIdUseCase,
    GetWorkspaceByOwnerUseCase,
    UpdateWorkspaceUseCase,
)

workspace_router = APIRouter()


@workspace_router.post(
    '/create_workspace',
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_workspace(
    body: CreateWorkspaceDTO, use_case: FromDishka[CreateWorkspaceUseCase]
) -> dict[str, str]:
    request = CreateWorkspaceAppDTO(**body.model_dump())  # type: ignore
    await use_case.execute(request)

    return {'redirect_url': '/'}


@workspace_router.get(
    '/{workspace_id}', status_code=status.HTTP_200_OK, response_model=ResponseWorkspaceDTO
)
@inject
async def get_workspace_by_id(
    workspace_id: WorkspaceId, use_case: FromDishka[GetWorkspaceByIdUseCase]
) -> ResponseWorkspaceDTO:
    try:
        response = await use_case.execute(workspace_id)
    except WorkspaceException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{str(e)}')

    return ResponseWorkspaceDTO(**response.__dict__)


@workspace_router.get(
    '/', status_code=status.HTTP_200_OK, response_model=list[ResponseWorkspaceDTO]
)
@inject
async def get_workspaces_by_owner_id(
    owner_id: OwnerId, use_case: FromDishka[GetWorkspaceByOwnerUseCase]
) -> list[ResponseWorkspaceDTO]:
    try:
        response = await use_case.execute(owner_id)
    except WorkspaceException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{str(e)}')

    return [ResponseWorkspaceDTO(**workspace.__dict__) for workspace in response]


@workspace_router.patch('/{workspace_id}')
@inject
async def update_workspace(
    body: UpdateWorkspaceDTO,
    workspace_id: WorkspaceId,
    use_case: FromDishka[UpdateWorkspaceUseCase],
) -> dict[str, str]:
    request = UpdateWorkspaceAppDTO(**body.model_dump(exclude_none=True))  # type: ignore
    try:
        await use_case.execute(workspace_id, request)
    except WorkspaceException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{str(error)}')

    return {'redirect_url': '/'}


@workspace_router.delete('/{workspace_id}', status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_workspace(
    workspace_id: WorkspaceId, use_case: FromDishka[DeleteWorkspaceUseCase]
) -> dict[str, str]:
    try:
        await use_case.execute(workspace_id)
    except WorkspaceException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{str(error)}')
    return {'redirect_url': '/'}
