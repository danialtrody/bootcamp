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
    
    async def find_by_email(self, session: AsyncSession, email: str) -> Student | None:
        result = await session.scalars(
            select(Student)
            .where(Student.email == email)
        )
        return result.first() 
    
    async def find_by_last_name(self, session: AsyncSession, last_name: str) -> list[Student]:
        result = await session.scalars(
            select(Student)
            .where(Student.last_name == last_name)
        )
        return result.all()
    
    async def find_by_partial_name(partial_name: str) -> list[Student]:
        pass