from src.apps.comment import CommentOutDto, UpdateCommentDto
from src.apps.comment.mapper import CommentMapper
from src.apps.comment.domain import CommentId, Content, ICommentRepository, Interactor


class UpdateCommentInteractor(Interactor[UpdateCommentDto, CommentOutDto]):

    def __init__(
        self,
        comment_repository: ICommentRepository,
    ):
        self._repository = comment_repository

    async def execute(self, request: UpdateCommentDto) -> CommentOutDto:
        updated_comment = await self._repository.update_comment(
            comment_id=CommentId(request.comment_id), new_content=Content(request.new_content)
        )
        return CommentMapper.entity_to_dto(updated_comment)
