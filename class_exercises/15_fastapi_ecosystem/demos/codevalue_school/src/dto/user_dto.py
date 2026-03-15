import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from src.constants import UserRole


class UserBaseDTO(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(default=UserRole.STUDENT.value)
    disabled: bool = Field(default=False)

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        if value not in UserRole.values():
            allowed = ", ".join(UserRole.values())
            raise ValueError(f"Role must be one of: {allowed}")
        return value


class UserCreateDTO(UserBaseDTO):
    password: str = Field(..., min_length=8)


class UserResponseDTO(UserBaseDTO):
    id: int
    created_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)


class LoginDTO(BaseModel):
    email: EmailStr
    password: str
