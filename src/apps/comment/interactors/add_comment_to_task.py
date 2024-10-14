from src.apps.comment import AddCommentToTaskDto, CommentOutDto
from src.apps.comment.domain import (
    AuthorId,
    CommentEntity,
    CommentId,
    Content,
    ICommentRepository,
    Interactor,
    TaskId,
)


class AddCommentToTaskInteractor(Interactor[AddCommentToTaskDto, CommentOutDto]):

    def __init__(self, comment_repository: ICommentRepository[CommentId, CommentEntity]):
        self._repository = comment_repository

    def execute(self, request: AddCommentToTaskDto) -> CommentOutDto:
        comment_entity = CommentEntity.create_for_entity(
            author_id=AuthorId(request.author_id),
            feature_id=request.feature_id,
            task_id=TaskId(request.task_id),
            content=Content(request.content),
        )

        c: CommentEntity = self._repository.save(comment_entity)
        response_dto: CommentOutDto = c.to_dto()
        return response_dto
