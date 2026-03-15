import json
from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
import sqlalchemy
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.app import app as fastapi_app
from src.auth.password_utils import hash_password
from src.database import Base, async_session_maker, engine
from src.models import Student, User
from src.secrets_accessor import get_secrets_accessor


def _load_fixture(name: str) -> list[dict[str, Any]]:
    with open(f"tests/fixtures/mock_{name}.json", "r") as fixture_file:
        return json.load(fixture_file)  # type: ignore[no-any-return]


def _build_user_records(raw_users: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "email": raw_user["email"],
            "first_name": raw_user["first_name"],
            "last_name": raw_user["last_name"],
            "password_hash": hash_password(raw_user["password"]),
            "role": raw_user["role"],
            "disabled": raw_user.get("disabled", False),
        }
        for raw_user in raw_users
    ]


async def _recreate_database(db_name: str, admin_url: str) -> None:
    """Drop and recreate the named test database."""
    admin_engine = create_async_engine(admin_url)
    async with admin_engine.connect() as conn:
        await conn.execute(sqlalchemy.text(f"DROP DATABASE IF EXISTS {db_name};"))
        await conn.execute(sqlalchemy.text(f"CREATE DATABASE {db_name};"))
    await admin_engine.dispose()


async def _build_schema() -> None:
    """Drop and recreate all ORM tables."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


async def _seed_fixtures() -> None:
    """Insert fixture records into the test database."""
    raw_users = _load_fixture("users")
    users = _build_user_records(raw_users)
    students = _load_fixture("students")
    async with async_session_maker() as db_session:
        await db_session.execute(sqlalchemy.insert(User).values(users))
        await db_session.execute(sqlalchemy.insert(Student).values(students))
        await db_session.commit()


async def _drop_database(db_name: str, admin_url: str) -> None:
    """Drop the named test database."""
    admin_engine = create_async_engine(admin_url)
    async with admin_engine.connect() as conn:
        await conn.execute(sqlalchemy.text(f"DROP DATABASE IF EXISTS {db_name};"))
    await admin_engine.dispose()


@pytest_asyncio.fixture(loop_scope="session", autouse=True)
async def prepare_database() -> AsyncGenerator[None, None]:
    """Setup and cleanup MySQL test database for the entire test session."""
    secrets = get_secrets_accessor()
    db_user = secrets.get_secret("DB_USER")
    db_pass = secrets.get_secret("DB_PASS")
    db_host = secrets.get_secret("DB_HOST")
    db_port = secrets.get_secret("DB_PORT")
    db_name = secrets.get_secret("DB_NAME")
    admin_url = f"mysql+aiomysql://{db_user}:{db_pass}@{db_host}:{db_port}"

    await _recreate_database(db_name, admin_url)
    await _build_schema()
    await _seed_fixtures()

    yield

    await _drop_database(db_name, admin_url)


@pytest.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Provide an httpx AsyncClient wired to the FastAPI app for each test."""
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a raw SQLAlchemy AsyncSession for direct DB assertions."""
    async with async_session_maker() as db_session:
        yield db_session
