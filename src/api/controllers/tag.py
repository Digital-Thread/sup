from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status, Path

from src.api.dtos.tag import CreateTagDTO, TagResponseDTO, UpdateTagDTO
from src.apps.workspace.dtos.tag_dtos import (
    CreateTagAppDTO,
    UpdateTagAppDTO,
)
from src.apps.workspace.exceptions.tag_exceptions import TagException
from src.apps.workspace.interactors.tag_interactors import (
    CreateTagInteractor,
    DeleteTagInteractor,
    GetTagByWorkspaceInteractor,
    UpdateTagInteractor,
    GetTagByIdInteractor,
)

tag_router = APIRouter(route_class=DishkaRoute)


@tag_router.post('', status_code=status.HTTP_201_CREATED)
async def create_tag(
    body: CreateTagDTO, interactor: FromDishka[CreateTagInteractor]
) -> dict[str, str]:
    request = CreateTagAppDTO(**body.model_dump())
    try:
        await interactor.execute(request)
    except TagException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return {'redirect_url': '/'}


@tag_router.get('/', status_code=status.HTTP_200_OK, response_model=list[TagResponseDTO])
async def get_tags_by_workspace_id(
    interactor: FromDishka[GetTagByWorkspaceInteractor]
) -> list[TagResponseDTO]:
    try:
        response = await interactor.execute()
    except TagException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return [TagResponseDTO(**tag.__dict__) for tag in response]


@tag_router.get('/{tag_id}', status_code=status.HTTP_200_OK, response_model=TagResponseDTO)
async def get_tag_by_id(
        tag_id: Annotated[int, Path()],
        interactor: FromDishka[GetTagByIdInteractor]
) -> TagResponseDTO:
    try:
        response = await interactor.execute(tag_id)
    except TagException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    else:
        return TagResponseDTO(**response.__dict__)



@tag_router.patch('/{tag_id}', status_code=status.HTTP_200_OK)
async def update_tag(
    body: UpdateTagDTO,
    tag_id: int,
    interactor: FromDishka[UpdateTagInteractor],
) -> dict[str, str]:
    request = UpdateTagAppDTO(**body.model_dump(exclude_none=True), id=tag_id)
    try:
        await interactor.execute(request)
    except TagException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return {'redirect_url': '/'}


@tag_router.delete('/{tag_id}')
async def delete_tag_by_id(
    tag_id: int, interactor: FromDishka[DeleteTagInteractor]
) -> dict[str, str]:
    try:
        await interactor.execute(tag_id)
    except TagException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return {'redirect_url': '/'}
