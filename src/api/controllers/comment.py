from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path, Query, status

from src.api.dtos import (
    CommentResponseDto,
    CreateCommentForFeatureDto,
    CreateCommentForTaskDto,
    UpdateCommentRequestDto,
)
from src.apps.comment import (
    AddCommentDto,
    CommentOutDto,
    CreateCommentInteractor,
    DeleteCommentDto,
    DeleteCommentInteractor,
    FetchTaskCommentDto,
    GetCommentsByFeatureIdInteractor,
    GetCommentsByTaskIdInteractor,
    UpdateCommentDto,
    UpdateCommentInteractor,
)
from src.apps.comment.dtos import FetchFeatureCommentDto

comment_router = APIRouter(route_class=DishkaRoute)


def dto_mapper(response: CommentOutDto) -> CommentResponseDto:
    return CommentResponseDto(**response.__dict__)


def list_dto_mapper(responses: list[CommentOutDto]) -> list[CommentResponseDto]:
    return [dto_mapper(response) for response in responses]


@comment_router.post(
    '/task',
    response_model=None,
    status_code=status.HTTP_201_CREATED,
)
async def add_comment_to_task(
    body: CreateCommentForTaskDto, interactor: FromDishka[CreateCommentInteractor]
) -> None:
    request = AddCommentDto(
        user_id=body.user_id,
        task_id=body.task_id,
        feature_id=None,
        content=body.content,
    )
    await interactor.execute(request=request)


@comment_router.post(
    '/feature',
    response_model=None,
    status_code=status.HTTP_201_CREATED,
)
async def add_comment_to_feature(
    body: CreateCommentForFeatureDto,
    interactor: FromDishka[CreateCommentInteractor],
) -> None:
    request = AddCommentDto(
        user_id=body.user_id, task_id=None, feature_id=body.feature_id, content=body.content
    )
    await interactor.execute(request=request)


@comment_router.get(
    '/tasks/{task_id}',
    response_model=list[CommentResponseDto],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_task_comments(
    interactor: FromDishka[GetCommentsByTaskIdInteractor],
    task_id: Annotated[int, Path()],
    page: int = Query(1, description='Page number', ge=1),
    page_size: int = Query(10, description='Number of comments per page', ge=1, le=100),
) -> list[CommentResponseDto]:
    response = await interactor.execute(
        request=FetchTaskCommentDto(page=page, page_size=page_size, task_id=task_id)
    )
    return list_dto_mapper(responses=response)


@comment_router.get(
    '/features/{feature_id}',
    response_model=list[CommentResponseDto],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_feature_comments(
    interactor: FromDishka[GetCommentsByFeatureIdInteractor],
    feature_id: Annotated[int, Path()],
    page: int = Query(1, description='Page number', ge=1),
    page_size: int = Query(10, description='Number of comments per page', ge=1, le=100),
) -> list[CommentResponseDto]:
    response = await interactor.execute(
        request=FetchFeatureCommentDto(feature_id=feature_id, page=page, page_size=page_size),
    )
    return list_dto_mapper(responses=response)


@comment_router.patch(
    '/{comment_id}',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_comment(
    comment_id: Annotated[int, Path()],
    body: UpdateCommentRequestDto,
    interactor: FromDishka[UpdateCommentInteractor],
) -> None:
    await interactor.execute(
        request=UpdateCommentDto(comment_id=comment_id, new_content=body.new_content)
    )


@comment_router.delete(
    '/{comment_id}',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
    comment_id: Annotated[int, Path()],
    interactor: FromDishka[DeleteCommentInteractor],
) -> None:
    await interactor.execute(request=DeleteCommentDto(comment_id=comment_id))
