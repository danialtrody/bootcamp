from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.constants import UserRole
from src.database import Base

if TYPE_CHECKING:
    from src.models.auth_session import AuthSession

MAX_EMAIL_LENGTH = 100
MAX_NAME_LENGTH = 100
MAX_ROLE_LENGTH = 20
MAX_HASH_LENGTH = 255


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(MAX_EMAIL_LENGTH), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH))
    last_name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH))
    password_hash: Mapped[str] = mapped_column(String(MAX_HASH_LENGTH))
    role: Mapped[str] = mapped_column(String(MAX_ROLE_LENGTH), default=UserRole.STUDENT.value)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    auth_sessions: Mapped[list[AuthSession]] = relationship(
        "AuthSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email!r}, role={self.role!r})"
