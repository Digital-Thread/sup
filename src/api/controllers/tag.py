from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status

from src.api.dtos.tag_dtos import CreateTagDTO, ResponseTagDTO, UpdateTagDTO
from src.apps.workspace.dtos.tag_dtos import CreateTagAppDTO, UpdateTagAppDTO, GetTagsAppDTO, DeleteTagAppDTO
from src.apps.workspace.exceptions.tag_exceptions import TagException
from src.apps.workspace.interactors.tag_interactors import (
    CreateTagInteractor,
    DeleteTagInteractor,
    GetTagByWorkspaceInteractor,
    UpdateTagInteractor,
)

tag_router = APIRouter(route_class=DishkaRoute)


@tag_router.post('', status_code=status.HTTP_201_CREATED)
async def create_tag(body: CreateTagDTO, interactor: FromDishka[CreateTagInteractor]) -> dict[str, str]:
    request = CreateTagAppDTO(**body.model_dump())
    try:
        await interactor.execute(request)
    except TagException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return {'redirect_url': '/'}


@tag_router.get('/', status_code=status.HTTP_200_OK, response_model=list[ResponseTagDTO])
async def get_tags_by_workspace_id(
    workspace_id: UUID, interactor: FromDishka[GetTagByWorkspaceInteractor]
) -> list[ResponseTagDTO]:
    try:
        response = await interactor.execute(GetTagsAppDTO(workspace_id=workspace_id))
    except TagException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return [ResponseTagDTO(**tag.__dict__) for tag in response]


@tag_router.patch('/{workspace_id}/{tag_id}', status_code=status.HTTP_200_OK)
async def update_tag(
    body: UpdateTagDTO,
    workspace_id: UUID,
    tag_id: int,
    interactor: FromDishka[UpdateTagInteractor],
) -> dict[str, str]:
    request = UpdateTagAppDTO(**body.model_dump(exclude_none=True), id=tag_id, workspace_id=workspace_id)
    try:
        await interactor.execute(request)
    except TagException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return {'redirect_url': '/'}


@tag_router.delete('/{workspace_id}/{tag_id}')
async def delete_tag_by_id(
    tag_id: int, workspace_id: UUID, interactor: FromDishka[DeleteTagInteractor]
) -> dict[str, str]:
    try:
        await interactor.execute(DeleteTagAppDTO(id=tag_id, workspace_id=workspace_id))
    except TagException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return {'redirect_url': '/'}
