from datetime import timedelta

import pytest

from app.core.security import create_access_token, decode_token, get_password_hash, verify_password


def test_password_hash_round_trip():
    password = "strong-password"
    hashed = get_password_hash(password)

    assert hashed != password
    assert verify_password(password, hashed) is True


def test_decode_token_returns_subject():
    token = create_access_token("admin@ab-agency.com", timedelta(minutes=5))

    payload = decode_token(token)

    assert payload["sub"] == "admin@ab-agency.com"


def test_decode_token_rejects_invalid_token():
    with pytest.raises(ValueError):
        decode_token("not-a-token")