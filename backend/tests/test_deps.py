import pytest
from fastapi import HTTPException

from app.api.deps import require_admin, require_staff
from app.core.security import create_access_token


def test_require_staff_accepts_editor(editor_user):
    assert require_staff(editor_user) == editor_user


def test_require_admin_rejects_non_admin(viewer_user):
    with pytest.raises(HTTPException) as exc:
        require_admin(viewer_user)

    assert exc.value.status_code == 403


def test_auth_headers_can_be_built_from_token(admin_user):
    token = create_access_token(admin_user.email)

    assert token