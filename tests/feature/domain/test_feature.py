import uuid
from datetime import datetime

from apps.feature.domain.entities.feature import Feature
from apps.feature.domain.entities.feature import Priority
from apps.feature.domain.entities.feature import Status


def test_feature_entity_init():
    project_id = uuid.uuid4()
    owner_id = uuid.uuid4()
    _id = uuid.uuid4()
    dt = datetime.now()

    feature = Feature(
        'New awesome feature',
        project_id,
        owner_id,
        id=_id,
        created_at=dt
    )

    assert feature.name == 'New awesome feature'
    assert feature.project_id == project_id
    assert feature.owner_id == owner_id
    assert feature.assigned_to is None
    assert feature.description is None
    assert feature.priority == Priority.NO_PRIORITY
    assert feature.status == Status.NEW
    assert feature.id == _id
    assert feature.created_at == dt
