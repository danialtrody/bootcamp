from typing import Any

from fastapi import APIRouter, Body, HTTPException, status

from src.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/")
async def get_students() -> list[dict[str, Any]]:
    service = StudentService()
    return await service.get_all_students()


@router.get("/{student_id}")
async def get_student(student_id: int) -> dict[str, Any]:
    service = StudentService()
    student = await service.get_student_by_id(student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )
    return student


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_student(student_data: dict[str, Any] = Body(...)) -> dict[str, Any]:
    service = StudentService()
    try:
        new_student = await service.create_student(student_data)
        return new_student
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
