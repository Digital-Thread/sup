from src.apps.comment.exceptions import CommentRepositoryError, CommentNotFoundError, InvalidContentError
from src.apps.comment import CommentOutDto, UpdateCommentDto
from src.apps.comment.mapper import CommentMapper
from src.apps.comment.domain import CommentId
from src.apps.comment.interactors.base_interactor import BaseInteractor
from src.apps.comment.repository import ICommentRepository


class UpdateCommentInteractor(BaseInteractor):

    def __init__(
            self,
            comment_repository: ICommentRepository,
    ):
        self._repository = comment_repository

    async def execute(self, request: UpdateCommentDto) -> CommentOutDto:
        try:
            comment = await self._repository.get_by_id(comment_id=CommentId(request.comment_id))
        except CommentRepositoryError as e:
            raise CommentNotFoundError()

        try:
            comment.update_content(new_content=request.new_content)
        except InvalidContentError as e:
            raise
        updated_comment = await self._repository.update_comment(comment=comment)
        return CommentMapper.entity_to_dto(updated_comment)
