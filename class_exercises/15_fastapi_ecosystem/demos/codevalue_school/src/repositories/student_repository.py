from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.student import Student


class StudentRepository:

    async def get_by_email(self, session: AsyncSession, email: str) -> Student | None:
        result = await session.execute(select(Student).where(Student.email == email))
        return result.scalar_one_or_none()

    async def get_all(self, session: AsyncSession) -> list[Student]:
        result = await session.scalars(select(Student))
        return list(result.all())

    async def get_by_id(self, session: AsyncSession, student_id: int) -> Student | None:
        return await session.get(Student, student_id)

    async def create(self, session: AsyncSession, student: Student) -> Student:
        session.add(student)
        await session.flush()
        await session.refresh(student)
        return student

    async def update(self, session: AsyncSession, student: Student, data: dict) -> Student:
        for key, value in data.items():
            setattr(student, key, value)
        await session.flush()
        await session.refresh(student)
        return student

    async def delete(self, session: AsyncSession, student: Student) -> None:
        await session.delete(student)
        await session.flush()
