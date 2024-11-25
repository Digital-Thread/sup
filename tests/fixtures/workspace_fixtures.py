from uuid import uuid4, UUID

import pytest

from src.apps.workspace.domain.types_ids import WorkspaceId, OwnerId, MemberId, InviteId


@pytest.fixture(scope="module")
def workspace_id() -> WorkspaceId:
    return WorkspaceId(uuid4())


@pytest.fixture(scope="module")
def owner_id() -> OwnerId:
    return OwnerId(uuid4())


@pytest.fixture()
def two_member_ids() -> list[MemberId]:
    return [MemberId(uuid4()), MemberId(uuid4())]


@pytest.fixture(scope="module")
def invite_code() -> UUID:
    return uuid4()
