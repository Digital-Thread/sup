from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request, status, Query

from src.api.dtos.workspace_invite_dtos import (
    ResponseWorkspaceInviteDTO,
    UpdateWorkspaceInviteDTO,
)
from src.apps.workspace.dtos.workspace_invite_dtos import UpdateWorkspaceInviteAppDTO, GetWorkspaceInvitesDTO
from src.apps.workspace.interactors.workspace_invite_interactors import (
    CreateWorkspaceInviteInteractor,
    DeleteWorkspaceInviteInteractor,
    GetWorkspaceInvitesByWorkspaceInteractor,
    UpdateWorkspaceInviteInteractor,
)
from src.providers.context import WorkspaceContext

workspace_invite_router = APIRouter(route_class=DishkaRoute)


@workspace_invite_router.post('', status_code=status.HTTP_201_CREATED)
async def create_workspace_invite(
    interactor: FromDishka[CreateWorkspaceInviteInteractor], context: FromDishka[WorkspaceContext]
) -> None:
    await interactor.execute(workspace_id=context.workspace_id)


@workspace_invite_router.get(
    '/', status_code=status.HTTP_200_OK, response_model=list[ResponseWorkspaceInviteDTO]
)
async def get_invites_in_workspace(
    request: Request,
    interactor: FromDishka[GetWorkspaceInvitesByWorkspaceInteractor],
    context: FromDishka[WorkspaceContext],
    page: int = Query(1, description='Page number', ge=1),
    page_size: int = Query(10, description='Number of workspace invites per page', ge=5, le=100)
) -> list[ResponseWorkspaceInviteDTO]:
    workspace_invites = await interactor.execute(
        GetWorkspaceInvitesDTO(workspace_id=context.workspace_id, page=page, page_size=page_size)
    )
    return [
        ResponseWorkspaceInviteDTO(
            **invite.__dict__,
            url=f'{request.url_for('create_user_by_invite', invite_token=invite.code)}',
        )
        for invite in workspace_invites
    ]


@workspace_invite_router.patch('/{workspace_invite}', status_code=status.HTTP_204_NO_CONTENT)
async def update_status_invite(
    body: UpdateWorkspaceInviteDTO,
    workspace_invite_id: int,
    interactor: FromDishka[UpdateWorkspaceInviteInteractor],
    context: FromDishka[WorkspaceContext],
) -> None:
    workspace_invite_update_data = UpdateWorkspaceInviteAppDTO(
        **body.model_dump(exclude_none=True),
        id_=workspace_invite_id,
        workspace_id=context.workspace_id,
    )
    await interactor.execute(workspace_invite_update_data)


@workspace_invite_router.delete('/{workspace_invite_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_by_id(
    workspace_invite_id: int,
    interactor: FromDishka[DeleteWorkspaceInviteInteractor],
    context: FromDishka[WorkspaceContext],
) -> None:
    await interactor.execute(
        workspace_invite_id=workspace_invite_id, workspace_id=context.workspace_id
    )
