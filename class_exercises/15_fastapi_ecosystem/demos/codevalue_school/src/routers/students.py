from fastapi import APIRouter, status

from src.dependencies import AdminDep, CurrentActiveUserDep, StudentServiceDep
from src.dto.student_dto import StudentCreateDTO, StudentResponseDTO, StudentUpdateDTO
from src.infrastructure.handle_exceptions_decorator import handle_exceptions
from src.models.user import User

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/", response_model=list[StudentResponseDTO])
@handle_exceptions()
async def get_students(service: StudentServiceDep, _admin: AdminDep) -> list[StudentResponseDTO]:
    return await service.get_all_students()


@router.get("/{student_id}", response_model=StudentResponseDTO)
@handle_exceptions()
async def get_student(
    student_id: int,
    service: StudentServiceDep,
    current_user: CurrentActiveUserDep,
) -> StudentResponseDTO:
    return await service.get_student_by_id(student_id, current_user)


@router.post("/", response_model=StudentResponseDTO, status_code=status.HTTP_201_CREATED)
@handle_exceptions()
async def create_student(
    data: StudentCreateDTO,
    service: StudentServiceDep,
    _admin: AdminDep,
) -> StudentResponseDTO:
    return await service.create_student(data)


@router.put("/{student_id}", response_model=StudentResponseDTO)
@handle_exceptions()
async def update_student(
    student_id: int,
    data: StudentUpdateDTO,
    service: StudentServiceDep,
    _admin: AdminDep,
) -> StudentResponseDTO:
    return await service.update_student(student_id, data)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_exceptions()
async def delete_student(
    student_id: int, service: StudentServiceDep, _admin: AdminDep
) -> None:
    await service.delete_student(student_id)
