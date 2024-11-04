from typing import NewType
from uuid import UUID

WorkspaceId = NewType('WorkspaceId', UUID)
OwnerId = NewType('OwnerId', UUID)
ProjectId = NewType('ProjectId', int)
FeatureId = NewType('FeatureId', int)
ParticipantId = NewType('ParticipantId', UUID)
AssignedId = NewType('AssignedId', UUID)
