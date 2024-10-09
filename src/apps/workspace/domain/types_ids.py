from typing import NewType
from uuid import UUID

WorkspaceId = NewType('WorkspaceId', UUID)
InviteId = NewType('InviteId', int)
OwnerId = NewType('OwnerId', UUID)
ProjectId = NewType('ProjectId', int)
FeatureId = NewType('FeatureId', int)
TaskId = NewType('TaskId', int)
MeetId = NewType('MeetId', int)
RoleId = NewType('RoleId', int)
TagId = NewType('TagId', int)
CategoryId = NewType('CategoryId', int)
MemberId = NewType('MemberId', UUID)
