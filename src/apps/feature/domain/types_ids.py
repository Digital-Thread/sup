from typing import NewType
from uuid import UUID

FeatureId = NewType('FeatureId', int)
OwnerId = NewType('OwnerId', UUID)
ProjectId = NewType('ProjectId', int)
TaskId = NewType('TaskId', int)
TagId = NewType('TagId', int)
UserId = NewType('UserId', UUID)
WorkspaceId = NewType('WorkspaceId', UUID)
