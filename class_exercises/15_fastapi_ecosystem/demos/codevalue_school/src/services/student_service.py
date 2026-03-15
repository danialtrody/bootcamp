import logging
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.constants import UserRole
from src.database import async_session_maker
from src.dto.student_dto import StudentCreateDTO, StudentResponseDTO, StudentUpdateDTO
from src.exceptions import StudentAlreadyExistsException, StudentNotFoundException
from src.models.student import Student
from src.models.user import User
from src.repositories.student_repository import StudentRepository

logger = logging.getLogger(__name__)


def _student_to_dto(student: Student) -> StudentResponseDTO:
    return StudentResponseDTO.model_validate(student)


def _is_admin(user: User) -> bool:
    return user.role == UserRole.ADMIN.value


class StudentService:

    def __init__(
        self,
        repo: Optional[StudentRepository] = None,
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
    ) -> None:
        self.repo = repo or StudentRepository()
        self.session_maker = session_maker or async_session_maker

    async def get_all_students(self) -> list[StudentResponseDTO]:
        logger.info("Fetching all students")
        async with self.session_maker() as session:
            students = await self.repo.get_all(session)
            return [_student_to_dto(student) for student in students]

    async def get_student_by_id(
        self, student_id: int, current_user: Optional[User] = None
    ) -> StudentResponseDTO:
        logger.info(f"Fetching student id={student_id}")
        async with self.session_maker() as session:
            student = await self.repo.get_by_id(session, student_id)
            if student is None:
                logger.warning(f"Student not found id={student_id}")
                raise StudentNotFoundException(f"Student {student_id} not found")
            if current_user is not None and not _is_admin(current_user):
                if student.user_id != current_user.id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access denied",
                    )
            return _student_to_dto(student)

    async def create_student(self, data: StudentCreateDTO) -> StudentResponseDTO:
        logger.info(f"Creating student email={data.email}")
        async with self.session_maker() as session:
            async with session.begin():
                existing = await self.repo.get_by_email(session, data.email)
                if existing is not None:
                    logger.warning(f"Student already exists email={data.email}")
                    raise StudentAlreadyExistsException(
                        f"Student with email {data.email} already exists"
                    )
                student = Student(
                    first_name=data.first_name,
                    last_name=data.last_name,
                    email=data.email,
                    birth_date=data.birth_date,
                )
                result = await self.repo.create(session, student)
            return _student_to_dto(result)

    async def update_student(self, student_id: int, data: StudentUpdateDTO) -> StudentResponseDTO:
        logger.info(f"Updating student id={student_id}")
        async with self.session_maker() as session:
            async with session.begin():
                student = await self.repo.get_by_id(session, student_id)
                if student is None:
                    logger.warning(f"Student not found id={student_id}")
                    raise StudentNotFoundException(f"Student {student_id} not found")
                result = await self.repo.update(session, student, data.model_dump())
            return _student_to_dto(result)

    async def delete_student(self, student_id: int) -> None:
        logger.info(f"Deleting student id={student_id}")
        async with self.session_maker() as session:
            async with session.begin():
                student = await self.repo.get_by_id(session, student_id)
                if student is None:
                    logger.warning(f"Student not found id={student_id}")
                    raise StudentNotFoundException(f"Student {student_id} not found")
                await self.repo.delete(session, student)


def get_student_service() -> StudentService:
    return StudentService(StudentRepository())
