import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.api.deps import get_db
from app.db.base import Base

# sql-тесты
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL)
TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

@pytest_asyncio.fixture(autouse=True)
async def prepare_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client():
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()

# Успешные тесты

async def test_register_success(client):
    response = await client.post("/auth/register", json={
        "email": "ivankiriyan@email.com",
        "password": "passwordsix-seven"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "ivankiriyan@email.com"
    assert data["role"] == "user"
    assert "id" in data
    assert "password_hash" not in data

async def test_login_success(client):
    await client.post("/auth/register", json={
        "email": "ivankiriyan@email.com",
        "password": "passwordsix-seven"
    })
    response = await client.post("/auth/login", data={
        "username": "ivankiriyan@email.com",
        "password": "passwordsix-seven"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_me_success(client):
    await client.post("/auth/register", json={
        "email": "ivankiriyan@email.com",
        "password": "passwordsix-seven"
    })
    login = await client.post("/auth/login", data={
        "username": "ivankiriyan@email.com",
        "password": "passwordsix-seven"
    })
    token = login.json()["access_token"]

    response = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "ivankiriyan@email.com"

# Неуспешные тесты

async def test_register_duplicate_email(client):
    await client.post("/auth/register", json={
        "email": "ivankiriyan@email.com",
        "password": "passwordsix-seven"
    })
    response = await client.post("/auth/register", json={
        "email": "ivankiriyan@email.com",
        "password": "passwordsix-seven"
    })
    assert response.status_code == 409

async def test_login_wrong_password(client):
    await client.post("/auth/register", json={
        "email": "ivankiriyan@email.com",
        "password": "passwordsix-seven"
    })
    response = await client.post("/auth/login", data={
        "username": "ivankiriyan@email.com",
        "password": "passwordsix-seven67"
    })
    assert response.status_code == 401

async def test_me_no_token(client):
    response = await client.get("/auth/me")
    assert response.status_code == 401

async def test_me_invalid_token(client):
    response = await client.get(
        "/auth/me", headers={"Authorization": "Bearer totally.invalid.token"}
    )
    assert response.status_code == 401