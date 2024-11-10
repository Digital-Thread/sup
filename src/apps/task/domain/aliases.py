from typing import NewType
from uuid import UUID

TaskId = NewType('TaskId', int)
FeatureId = NewType('FeatureId', int)
TagId = NewType('TagId', int)
WorkspaceId = NewType('WorkspaceId', UUID)
OwnerId = NewType('OwnerId', UUID)
AssignedId = NewType('AssignedId', UUID)
