from src.apps.comment import CommentOutDto, CommentPaginationDto, FetchCommentDto
from src.apps.comment.converters import CommentMapper
from src.apps.comment.domain import (
    CommentEntity,
    CommentId,
    Content,
    ICommentRepository,
    Interactor,
)


class FetchCommentInteractor(Interactor[FetchCommentDto, CommentOutDto]):

    def __init__(self, comment_repository: ICommentRepository[Content, CommentId, CommentEntity]):
        self._repository = comment_repository

    async def execute(self, request: FetchCommentDto) -> CommentOutDto:
        comment = await self._repository.fetch_by_id(comment_id=CommentId(request.comment_id))
        return CommentMapper.entity_to_dto(comment)


class FetchAllCommentsInteractor(Interactor[CommentPaginationDto, list[CommentOutDto]]):
    def __init__(self, comment_repository: ICommentRepository[Content, CommentId, CommentEntity]):
        self._repository = comment_repository

    async def execute(self, request: CommentPaginationDto) -> list[CommentOutDto]:
        comments = await self._repository.fetch_all(page=request.page, page_size=request.page_size)
        return [CommentMapper.entity_to_dto(comment) for comment in comments]
