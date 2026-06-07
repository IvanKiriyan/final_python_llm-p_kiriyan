import pytest
from jose import jwt
from app.core.config import settings
from app.core.jwt import decode_and_validate

def make_token(payload: dict) -> str:
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def test_valid_token():
    token = make_token({"sub": "123", "role": "user", "exp": 9999999999})
    payload = decode_and_validate(token)
    assert payload["sub"] == "123"
    assert payload["role"] == "user"

def test_garbage_token():
    with pytest.raises(ValueError):
        decode_and_validate("not_a_token_at_all")

def test_expired_token():
    token = make_token({"sub": "123", "exp": 1})
    with pytest.raises(ValueError):
        decode_and_validate(token)

def test_missing_sub():
    token = make_token({"role": "user", "exp": 9999999999})
    with pytest.raises(ValueError):
        decode_and_validate(token)