import datetime
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.auth_session import AuthSession


class AuthSessionRepository:

    async def create(self, session: AsyncSession, auth_session: AuthSession) -> AuthSession:
        session.add(auth_session)
        await session.flush()
        await session.refresh(auth_session)
        return auth_session

    async def get_with_user(self, session: AsyncSession, session_id: str) -> Optional[AuthSession]:
        query = select(AuthSession).options(selectinload(AuthSession.user)).where(
            AuthSession.id == session_id
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def deactivate(self, session: AsyncSession, session_id: str) -> None:
        stmt = update(AuthSession).where(AuthSession.id == session_id).values(is_active=False)
        await session.execute(stmt)

    async def update_last_activity(self, session: AsyncSession, session_id: str) -> None:
        stmt = update(AuthSession).where(AuthSession.id == session_id).values(
            last_activity=datetime.datetime.utcnow()
        )
        await session.execute(stmt)
