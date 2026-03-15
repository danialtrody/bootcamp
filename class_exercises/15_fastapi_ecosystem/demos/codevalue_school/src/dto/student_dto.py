import datetime
from typing import Optional

from pydantic import BaseModel


class StudentBaseDTO(BaseModel):
    first_name: str
    last_name: str
    email: str
    birth_date: Optional[datetime.date] = None


class StudentCreateDTO(StudentBaseDTO):
    """DTO for creating a new student."""


class StudentUpdateDTO(StudentBaseDTO):
    """DTO for updating an existing student."""


class StudentResponseDTO(StudentBaseDTO):
    student_id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True
