from typing import NewType
from uuid import UUID

FeatureId = NewType('FeatureId', int)
OwnerId = NewType('OwnerId', UUID)
ProjectId = NewType('ProjectId', int)
TagId = NewType('TagId', int)
UserId = NewType('UserId', UUID)
