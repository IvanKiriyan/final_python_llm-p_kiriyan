import pytest
import fakeredis.aioredis
from jose import jwt
from app.core.config import settings

@pytest.fixture
async def fake_redis():
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    yield redis
    await redis.flushall()
    await redis.aclose()

@pytest.fixture
def valid_token():
    return jwt.encode(
        {"sub": "42", "role": "user", "exp": 9999999999},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALG,
    )