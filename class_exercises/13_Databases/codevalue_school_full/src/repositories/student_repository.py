from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.student import Student


class StudentRepository:

    async def get_all(self, session: AsyncSession) -> list[Student]:
        result = await session.scalars(select(Student))
        return list(result.all())

    async def get_by_id(self, session: AsyncSession, student_id: int) -> Student | None:
        return await session.get(Student, student_id)

    async def create(self, session: AsyncSession, student: Student) -> Student:
        session.add(student)
        await session.commit()
        await session.refresh(student)
        return student
