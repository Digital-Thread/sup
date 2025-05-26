from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path, Query, status

from src.api.dtos.tag import CreateTagRequestDTO, TagResponseDTO, UpdateTagDTO
from src.apps.workspace.dtos.tag_dtos import CreateTagDTO, GetTagsDTO, UpdateTagAppDTO
from src.apps.workspace.interactors.tag_interactors import (
    CreateTagInteractor,
    DeleteTagInteractor,
    GetTagByIdInteractor,
    GetTagByWorkspaceInteractor,
    UpdateTagInteractor,
)
from src.providers.context import WorkspaceContext

tag_router = APIRouter(route_class=DishkaRoute)


@tag_router.post('', status_code=status.HTTP_201_CREATED)
async def create_tag(
    body: CreateTagRequestDTO,
    interactor: FromDishka[CreateTagInteractor],
    context: FromDishka[WorkspaceContext],
) -> None:
    create_tag_data = CreateTagDTO(**body.model_dump(), workspace_id=context.workspace_id)
    await interactor.execute(create_tag_data=create_tag_data)


@tag_router.get('/', status_code=status.HTTP_200_OK, response_model=list[TagResponseDTO])
async def get_tags_in_workspace(
    interactor: FromDishka[GetTagByWorkspaceInteractor],
    context: FromDishka[WorkspaceContext],
    page: int = Query(1, description='Page number', ge=1),
    page_size: int = Query(10, description='Number of tags per page', ge=5, le=100),
) -> list[TagResponseDTO]:
    tags = await interactor.execute(
        GetTagsDTO(workspace_id=context.workspace_id, page=page, page_size=page_size)
    )
    return [TagResponseDTO.model_validate(tag) for tag in tags]


@tag_router.get('/{tag_id}', status_code=status.HTTP_200_OK, response_model=TagResponseDTO)
async def get_tag_by_id(
    tag_id: Annotated[int, Path()],
    interactor: FromDishka[GetTagByIdInteractor],
    context: FromDishka[WorkspaceContext],
) -> TagResponseDTO:
    tag = await interactor.execute(tag_id=tag_id, workspace_id=context.workspace_id)
    return TagResponseDTO.model_validate(tag)


@tag_router.patch('/{tag_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_tag(
    body: UpdateTagDTO,
    tag_id: int,
    interactor: FromDishka[UpdateTagInteractor],
    context: FromDishka[WorkspaceContext],
) -> None:
    updated_tag_data = UpdateTagAppDTO(
        **body.model_dump(exclude_none=True), id=tag_id, workspace_id=context.workspace_id
    )
    await interactor.execute(updated_tag_data=updated_tag_data)


@tag_router.delete('/{tag_id}')
async def delete_tag_by_id(
    tag_id: int, interactor: FromDishka[DeleteTagInteractor], context: FromDishka[WorkspaceContext]
) -> None:
    await interactor.execute(tag_id=tag_id, workspace_id=context.workspace_id)
