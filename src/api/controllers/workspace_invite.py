from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, HTTPException, Request, status

from src.api.dtos.workspace_invite_dtos import (
    ResponseWorkspaceInviteDTO,
    UpdateWorkspaceInviteDTO,
)
from src.apps.workspace.dtos.workspace_invite_dtos import (
    CreateWorkspaceInviteDTO,
    DeleteWorkspaceInviteAppDTO,
    GetWorkspaceInvitesAppDTO,
    UpdateWorkspaceInviteAppDTO,
)
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteException,
)
from src.apps.workspace.interactors.workspace_invite_interactors import (
    CreateWorkspaceInviteInteractor,
    DeleteWorkspaceInviteInteractor,
    GetWorkspaceInviteByWorkspaceInteractor,
    UpdateWorkspaceInviteInteractor,
)

workspace_invite_router = APIRouter(route_class=DishkaRoute)


@workspace_invite_router.post('', status_code=status.HTTP_201_CREATED)
async def create_workspace_invite(
    workspace_id: Annotated[UUID, Body(embed=True)],
    interactor: FromDishka[CreateWorkspaceInviteInteractor],
) -> dict[str, str]:
    try:
        await interactor.execute(CreateWorkspaceInviteDTO(workspace_id=workspace_id))
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
    interactor: FromDishka[GetWorkspaceInviteByWorkspaceInteractor],
) -> list[ResponseWorkspaceInviteDTO]:
    try:
        response = await interactor.execute(GetWorkspaceInvitesAppDTO(workspace_id=workspace_id))
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


@workspace_invite_router.patch('/{workspace_id}/{workspace_invite}', status_code=status.HTTP_200_OK)
async def update_status_invite(
    body: UpdateWorkspaceInviteDTO,
    workspace_id: UUID,
    workspace_invite_id: int,
    interactor: FromDishka[UpdateWorkspaceInviteInteractor],
) -> dict[str, str]:
    request = UpdateWorkspaceInviteAppDTO(
        **body.model_dump(exclude_none=True), id_=workspace_invite_id, workspace_id=workspace_id
    )

    try:
        await interactor.execute(request)
    except WorkspaceInviteException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    else:
        return {'redirect': '/'}


@workspace_invite_router.delete(
    '/{workspace_id}/{workspace_invite_id}', status_code=status.HTTP_200_OK
)
async def delete_category_by_id(
    workspace_invite_id: int,
    workspace_id: UUID,
    interactor: FromDishka[DeleteWorkspaceInviteInteractor],
) -> dict[str, str]:
    try:
        await interactor.execute(
            DeleteWorkspaceInviteAppDTO(id_=workspace_invite_id, workspace_id=workspace_id)
        )
    except WorkspaceInviteException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return {'redirect_url': '/'}
