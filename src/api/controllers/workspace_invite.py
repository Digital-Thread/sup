from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, HTTPException, Request, status

from src.api.dtos.workspace_invite_dtos import (
    ResponseWorkspaceInviteDTO,
    UpdateWorkspaceInviteDTO,
)
from src.apps.workspace.dtos.workspace_invite_dtos import UpdateWorkspaceInviteAppDTO
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteException,
)
from src.apps.workspace.use_cases.workspace_invite_use_cases import (
    CreateWorkspaceInviteUseCase,
    DeleteWorkspaceInviteUseCase,
    GetWorkspaceInviteByWorkspaceUseCase,
    UpdateWorkspaceInviteUseCase,
)

workspace_invite_router = APIRouter(route_class=DishkaRoute)


@workspace_invite_router.post('', status_code=status.HTTP_201_CREATED)
async def create_category(
    workspace_id: Annotated[UUID, Body(embed=True)],
    use_case: FromDishka[CreateWorkspaceInviteUseCase],
) -> dict[str, str]:
    try:
        await use_case.execute(workspace_id)
    except WorkspaceInviteException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    else:
        return {'redirect': '/'}


@workspace_invite_router.get(
    '/', status_code=status.HTTP_200_OK, response_model=list[ResponseWorkspaceInviteDTO]
)
async def get_invites_by_workspace_id(
    request: Request,
    workspace_id: UUID,
    use_case: FromDishka[GetWorkspaceInviteByWorkspaceUseCase],
) -> list[ResponseWorkspaceInviteDTO]:
    try:
        response = await use_case.execute(workspace_id)
    except WorkspaceInviteException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    else:
        return [
            ResponseWorkspaceInviteDTO(
                **invite.__dict__,
                url=f'{request.url_for('create_user_by_invite', invite_token=invite.code)}',
            )
            for invite in response
        ]


@workspace_invite_router.patch('/{workspace_invite}', status_code=status.HTTP_200_OK)
async def update_status_invite(
    body: UpdateWorkspaceInviteDTO,
    workspace_id: UUID,
    workspace_invite_id: int,
    use_case: FromDishka[UpdateWorkspaceInviteUseCase],
) -> dict[str, str]:
    request = UpdateWorkspaceInviteAppDTO(**body.model_dump(exclude_none=True))

    try:
        await use_case.execute(workspace_invite_id, workspace_id, request)
    except WorkspaceInviteException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    else:
        return {'redirect': '/'}


@workspace_invite_router.delete('/{workspace_invite}', status_code=status.HTTP_200_OK)
async def delete_category_by_id(
    invite_id: int,
    workspace_id: UUID,
    use_case: FromDishka[DeleteWorkspaceInviteUseCase],
) -> dict[str, str]:
    try:
        await use_case.execute(invite_id, workspace_id)
    except WorkspaceInviteException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return {'redirect_url': '/'}
