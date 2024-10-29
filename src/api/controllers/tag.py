from fastapi import APIRouter, status, HTTPException
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from src.api.dtos.tag_dtos import CreateTagDTO, ResponseTagDTO, UpdateTagDTO
from src.apps.workspace.domain.types_ids import WorkspaceId, TagId
from src.apps.workspace.dtos.tag_dtos import CreateTagAppDTO, UpdateTagAppDTO
from src.apps.workspace.exceptions.tag_exceptions import TagException
from src.apps.workspace.use_cases.tag_use_cases import (
    CreateTagUseCase, GetTagByWorkspaceUseCase, UpdateTagUseCase, DeleteTagUseCase
)

tag_router = APIRouter(route_class=DishkaRoute)


@tag_router.post('/create_tag', status_code=status.HTTP_201_CREATED)
async def create_tag(body: CreateTagDTO, use_case: FromDishka[CreateTagUseCase]):
    request = CreateTagAppDTO(**body.model_dump()) # type: ignore
    try:
        await use_case.execute(request)
    except TagException as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    return {'redirect_url': '/'}


@tag_router.get('/', status_code=status.HTTP_200_OK, response_model=list[ResponseTagDTO])
async def get_tags_by_workspace_id(workspace_id: WorkspaceId, use_case: FromDishka[GetTagByWorkspaceUseCase]) -> list[ResponseTagDTO]:
    try:
        response = await use_case.execute(workspace_id)
    except TagException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
    return [ResponseTagDTO(**tag.__dict__) for tag in response]


@tag_router.patch('/{tag_id}', status_code=status.HTTP_200_OK)
async def update_tag(body: UpdateTagDTO, workspace_id: WorkspaceId, tag_id: TagId, use_case: FromDishka[UpdateTagUseCase]) -> dict[str, str]:
    request = UpdateTagAppDTO(**body.model_dump(exclude_none=True))
    try:
        await use_case.execute(tag_id, workspace_id, request)
    except TagException as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    return {'redirect_url': '/'}


@tag_router.delete('/{tag_id}')
async def delete_tag_by_id(tag_id: TagId, workspace_id: WorkspaceId, use_case: FromDishka[DeleteTagUseCase]) -> dict[str, str]:
    try:
        await use_case.execute(tag_id, workspace_id)
    except TagException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
    return {'redirect_url': '/'}