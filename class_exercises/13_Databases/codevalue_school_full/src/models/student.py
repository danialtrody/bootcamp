import datetime

from sqlalchemy import Date, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

MAX_EMAIL_LENGTH = 255
MAX_NAME_LENGTH = 100


class Student(Base):
    __tablename__ = "students"

    student_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
    last_name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
    email: Mapped[str] = mapped_column(String(MAX_EMAIL_LENGTH), nullable=False, unique=True)
    birth_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
