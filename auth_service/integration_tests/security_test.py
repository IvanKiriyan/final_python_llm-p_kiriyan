import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_token


def test_hash_is_not_plain():
    hashed = hash_password("mypassword")
    assert hashed != "mypassword"


def test_verify_correct_password():
    hashed = hash_password("mypassword")
    assert verify_password("mypassword", hashed) is True


def test_verify_wrong_password():
    hashed = hash_password("mypassword")
    assert verify_password("wrongpassword", hashed) is False


def test_create_and_decode_token():
    token = create_access_token(sub="42", role="user")
    payload = decode_token(token)

    assert payload["sub"] == "42"
    assert payload["role"] == "user"
    assert "iat" in payload
    assert "exp" in payload