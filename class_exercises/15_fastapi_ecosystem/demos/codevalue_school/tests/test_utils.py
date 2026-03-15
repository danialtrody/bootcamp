"""Helper utilities for creating auth tokens and setting cookies in tests."""

import uuid
from datetime import UTC, datetime, timedelta

from httpx import AsyncClient
from sqlalchemy import select

from src.auth.jwt_utils import create_access_token
from src.constants import SESSION_EXPIRY_HOURS
from src.database import async_session_maker
from src.models.auth_session import AuthSession
from src.models.user import User

SESSION_COOKIE_NAME = "session_token"


async def create_auth_token_for_user(email: str) -> str:
    """Create a valid JWT session token for a test user identified by email."""
    session_id = str(uuid.uuid4())
    expires_at = datetime.now(UTC).replace(tzinfo=None) + timedelta(hours=SESSION_EXPIRY_HOURS)

    async with async_session_maker() as db_session:
        async with db_session.begin():
            result = await db_session.execute(select(User).where(User.email == email))
            user: User = result.scalar_one()
            auth_session = AuthSession(
                id=session_id,
                user_id=user.id,
                is_active=True,
                expires_at=expires_at,
                fingerprint=None,
            )
            db_session.add(auth_session)

    return create_access_token(session_id)


def set_auth_cookie(client: AsyncClient, token: str) -> None:
    """Set the session token cookie on an httpx AsyncClient."""
    client.cookies.set(SESSION_COOKIE_NAME, token)
