from typing import Any

from src.database import async_session_maker
from src.models.student import Student
from src.repositories.student_repository import StudentRepository
from typing import Optional


def _student_to_dict(student: Student) -> dict[str, Any]:
    return {
        "student_id": student.student_id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "email": student.email,
        "birth_date": student.birth_date,
        "created_at": student.created_at,
    }


class StudentService:

    def __init__(self, repository: Optional[StudentRepository] = None):
        self.repository = repository or StudentRepository()

    async def get_all_students(self) -> list[dict[str, Any]]:
        async with async_session_maker() as session:
            students = await self.repository.get_all(session)
            return [_student_to_dict(student) for student in students]

    async def get_student_by_id(self, student_id: int) -> dict[str, Any] | None:
        async with async_session_maker() as session:
            student = await self.repository.get_by_id(session, student_id)
            if student is None:
                return None
            return _student_to_dict(student)

    async def create_student(self, student_data: dict[str, Any]) -> dict[str, Any]:
        async with async_session_maker() as session:
            student = Student(
                first_name=student_data["first_name"],
                last_name=student_data["last_name"],
                email=student_data["email"],
                birth_date=student_data.get("birth_date"),
            )
            return _student_to_dict(await self.repository.create(session, student))

    async def get_student_by_email(self, email: str) -> Student:
        async with async_session_maker() as session:
            student = await self.repository.find_by_email(session, email)
            if student is None:
                return None
            return _student_to_dict(student)

    async def get_students_by_last_name(self, last_name: str) -> dict[str, Any]:
        async with async_session_maker() as session:
            students = await self.repository.find_by_last_name(session, last_name)
            if students is None:
                return None
            result = []
            
            for student in students:
                result.append(_student_to_dict(student))
            
            return result 