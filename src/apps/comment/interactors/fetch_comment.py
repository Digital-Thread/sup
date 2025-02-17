from src.apps.comment import (
    CommentOutDto,
    CommentPaginationDto,
    FetchCommentDto,
    FetchTaskCommentDto,
)
from src.apps.comment.mapper import CommentMapper
from src.apps.comment.domain import (
    CommentId,
    FeatureId,
    TaskId,
)
from src.apps.comment.interactors.base_interactor import Interactor
from src.apps.comment.repository import ICommentRepository
from src.apps.comment.dtos import FetchFeatureCommentDto


class FetchCommentInteractor(Interactor[FetchCommentDto, CommentOutDto]):

    def __init__(self, comment_repository: ICommentRepository):
        self._repository = comment_repository

    async def execute(self, request: FetchCommentDto) -> CommentOutDto:
        comment = await self._repository.fetch_by_id(comment_id=CommentId(request.comment_id))
        return CommentMapper.entity_to_dto(comment)


class FetchAllCommentsInteractor(Interactor[CommentPaginationDto, list[CommentOutDto]]):
    def __init__(self, comment_repository: ICommentRepository):
        self._repository = comment_repository

    async def execute(self, request: CommentPaginationDto) -> list[CommentOutDto]:
        comments = await self._repository.fetch_all(page=request.page, page_size=request.page_size)
        return [CommentMapper.entity_to_dto(comment) for comment in comments]


class FetchAllTaskCommentsInteractor(Interactor[FetchTaskCommentDto, list[CommentOutDto]]):

    def __init__(self, comment_repository: ICommentRepository):
        self._repository = comment_repository

    async def execute(self, request: FetchTaskCommentDto) -> list[CommentOutDto]:
        comments = await self._repository.fetch_task_comments(
            task_id=TaskId(request.task_id),
            page=request.page,
            page_size=request.page_size,
        )
        return [CommentMapper.entity_to_dto(comment) for comment in comments]


class FetchAllFeatureCommentsInteractor(Interactor[FetchFeatureCommentDto, list[CommentOutDto]]):
    def __init__(self, comment_repository: ICommentRepository):
        self._repository = comment_repository

    async def execute(self, request: FetchFeatureCommentDto) -> list[CommentOutDto]:
        comments = await self._repository.fetch_feature_comments(
            feature_id=FeatureId(request.feature_id),
            page=request.page,
            page_size=request.page_size,
        )
        return [CommentMapper.entity_to_dto(comment) for comment in comments]
