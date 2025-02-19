from typing import NewType
from uuid import UUID

CommentId = NewType('CommentId', int)
FeatureId = NewType('FeatureId', int)
AuthorId = NewType('AuthorId', UUID)
TaskId = NewType('TaskId', int)
