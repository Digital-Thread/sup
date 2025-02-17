from src.apps.comment import CommentOutDto
from src.apps.comment.domain import AuthorId, Content, FeatureId, TaskId
from src.apps.comment.domain.comment import CommentEntity
from src.apps.comment.dtos import BaseCommentDto


class CommentMapper:
    @staticmethod
    def entity_to_dto(entity: CommentEntity) -> CommentOutDto:
        return CommentOutDto(
            comment_id=entity.comment_id.value,
            task_id=entity.task_id.value if entity.task_id is not None else None,
            feature_id=entity.feature_id.value if entity.feature_id is not None else None,
            content=entity.content.value,
            user_id=entity.user_id.value,
            created_at=entity.created_at.value,
            updated_at=entity.updated_at.value,
        )

    @staticmethod
    def dto_to_entity(dto: BaseCommentDto) -> CommentEntity:
        return CommentEntity.create_for_entity(
            user_id=AuthorId(dto.user_id),
            task_id=TaskId(dto.task_id) if dto.task_id is not None else None,
            feature_id=FeatureId(dto.feature_id) if dto.feature_id is not None else None,
            content=Content(dto.content),
        )
