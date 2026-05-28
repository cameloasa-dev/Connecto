import asyncio

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from app.core.security import get_password_hash
from app.db.database import Base, get_db
from app.db.models import User
from app.main import app

# -----------------------------
# Test database (SQLite in-memory)
# -----------------------------
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# -----------------------------
# Event loop for async tests
# -----------------------------
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# -----------------------------
# Async engine for tests
# -----------------------------
@pytest_asyncio.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


# -----------------------------
# Prepare DB before tests
# -----------------------------
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# -----------------------------
# Database session per test
# -----------------------------
@pytest_asyncio.fixture
async def db_session(async_engine):
    # Start conexion for  test
    async with async_engine.connect() as connection:
        # Start a real transaction
        trans = await connection.begin()

        # Create a session bound to this transaction
        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
        )

        try:
            yield session
        finally:
            # Initial state for next test
            await trans.rollback()
            await session.close()


# -----------------------------
# FastAPI test client
# -----------------------------
@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# -----------------------------
# Helper: create test user
# -----------------------------
@pytest_asyncio.fixture
async def create_test_user(db_session):
    async def _create(username: str, password: str):
        hashed = get_password_hash(password)
        user = User(
            username=username,
            email=f"{username}@test.com",
            hashed_password=hashed,
            is_active=True,
        )
        db_session.add(user)
        await db_session.flush()
        await db_session.refresh(user)
        return user

    return _create
