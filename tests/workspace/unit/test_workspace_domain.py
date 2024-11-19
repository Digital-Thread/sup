from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest

from src.apps.workspace.domain.entities.workspace import Workspace
from src.apps.workspace.domain.types_ids import OwnerId

OWNER_ID = uuid4()
WORKSPACE_ID = uuid4()
MEMBER_1_ID = uuid4()
MEMBER_2_ID = uuid4()


@pytest.fixture()
def workspace_minimal():
    return Workspace(owner_id=OwnerId(uuid4()), _name='Minimal Workspace')


@pytest.fixture(
    params=[
        {
            'name': 'Full Workspace',
            'owner_id': OWNER_ID,
            'id': WORKSPACE_ID,
            'description': 'Full Workspace description',
            'logo': 'workspace_logo.png',
            'created_at': datetime.now(timezone.utc),
            'invite_ids': [1, 2, 3, 4, 5],
            'project_ids': [6, 7, 8, 9, 10],
            'meet_ids': [11, 12, 13, 14, 15],
            'tag_ids': [16, 17, 18, 19, 20],
            'role_ids': [21, 22, 23, 24, 25],
            'member_ids': [MEMBER_1_ID, MEMBER_2_ID],
        }
    ]
)
def workspace_full(request) -> Workspace:
    params = request.param
    return Workspace(
        owner_id=params['owner_id'],
        _name=params['name'],
        _id=params.get('id'),
        _description=params.get('description'),
        logo=params.get('logo'),
        invite_ids=params.get('invite_ids'),
        project_ids=params.get('project_ids'),
        meet_ids=params.get('meet_ids'),
        tag_ids=params.get('tag_ids'),
        role_ids=params.get('role_ids'),
        member_ids=params.get('member_ids'),
    )


class TestWorkspaceCreation:

    def test_workspace_creation_with_required_data(self, workspace_minimal):
        assert workspace_minimal.name == 'Minimal Workspace'
        assert isinstance(workspace_minimal.owner_id, UUID)

    def test_workspace_creation_with_full_data(self, workspace_full):
        assert workspace_full.name == 'Full Workspace'
        assert workspace_full.description == 'Full Workspace description'
        assert workspace_full.logo == 'workspace_logo.png'
        assert workspace_full.invite_ids == [1, 2, 3, 4, 5]
        assert workspace_full.project_ids == [6, 7, 8, 9, 10]
        assert workspace_full.meet_ids == [11, 12, 13, 14, 15]
        assert workspace_full.tag_ids == [16, 17, 18, 19, 20]
        assert workspace_full.role_ids == [21, 22, 23, 24, 25]
        assert workspace_full.member_ids == [MEMBER_1_ID, MEMBER_2_ID]

    def test_workspace_has_correct_default_values(self, workspace_minimal):
        assert workspace_minimal.description is None
        assert workspace_minimal.id is None
        assert workspace_minimal.logo is None
        assert isinstance(workspace_minimal.created_at, datetime)
        assert abs((workspace_minimal.created_at - datetime.now(timezone.utc)).total_seconds()) < 1
        assert workspace_minimal.invite_ids == []
        assert workspace_minimal.project_ids == []
        assert workspace_minimal.meet_ids == []
        assert workspace_minimal.tag_ids == []
        assert workspace_minimal.role_ids == []
        assert workspace_minimal.member_ids == []

    def test_workspace_creation_missing_required_fields(self):
        with pytest.raises(TypeError):
            Workspace()


class TestWorkspaceValidation:

    def test_valid_workspace_name(self, workspace_minimal):
        workspace_minimal.name = 'Another Valid Workspace'
        assert workspace_minimal.name == 'Another Valid Workspace'

    def test_valid_workspace_description(self, workspace_minimal):
        workspace_minimal.description = 'This is a valid workspace description.'
        assert workspace_minimal.description == 'This is a valid workspace description.'

    @pytest.mark.parametrize(
        'name, expected_error_message',
        [
            ('', 'Имя рабочего пространства должно содержать хотя бы одну букву'),
            (' ', 'Имя рабочего пространства должно содержать хотя бы одну букву'),
            ('Full Workspace@#$%^&*()+', 'Неверный формат названия рабочего пространства'),
        ],
    )
    def test_invalid_workspace_name(self, workspace_minimal, name, expected_error_message):

        with pytest.raises(ValueError, match=expected_error_message):
            workspace_minimal.name = name

    def test_invalid_workspace_description(self, workspace_minimal):
        with pytest.raises(
            ValueError,
            match=f'Длина описания рабочего пространства не должна превышать 500 символов.'
            f'И содержать только буквы латинского и русского алфавитов, включая символы пробела и -.',
        ):
            workspace_minimal.description = 'Full Workspace@#$%^&*()+'

    def test_max_workspace_name_length(self, workspace_minimal):
        valid_name = 'n' * 50
        workspace_minimal.name = valid_name
        assert workspace_minimal.name == valid_name

        with pytest.raises(ValueError, match=f'Неверный формат названия рабочего пространства'):
            workspace_minimal.name = 'n' * 51

    def test_max_workspace_description_length(self, workspace_minimal):
        valid_description = 'n' * 500
        workspace_minimal.description = valid_description
        assert workspace_minimal.description == valid_description

        with pytest.raises(
            ValueError,
            match=f'Длина описания рабочего пространства не должна превышать 500 символов.'
            f'И содержать только буквы латинского и русского алфавитов, включая символы пробела и -.',
        ):
            workspace_minimal.description = 'n' * 501

    def test_workspace_id_set_once_only(self, workspace_full):
        with pytest.raises(
            AttributeError, match='Идентификатор рабочего пространства уже установлен'
        ):
            workspace_full.id = uuid4()
