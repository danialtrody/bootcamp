from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.models.user import User

AUTH_SESSION_ID_LENGTH = 36


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    id: Mapped[str] = mapped_column(String(AUTH_SESSION_ID_LENGTH), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    last_activity: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fingerprint: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped[User] = relationship("User", back_populates="auth_sessions")

    def __repr__(self) -> str:
        return f"AuthSession(id={self.id!r}, user_id={self.user_id}, is_active={self.is_active})"
