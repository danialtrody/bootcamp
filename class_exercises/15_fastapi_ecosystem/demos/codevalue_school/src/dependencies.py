from typing import Annotated

from fastapi import Depends

from src.auth.auth_dependencies import (
    get_current_active_user,
    get_current_admin,
    get_current_user,
)
from src.models.user import User
from src.services.auth_service import AuthService, get_auth_service
from src.services.student_service import StudentService, get_student_service

StudentServiceDep = Annotated[StudentService, Depends(get_student_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

CurrentUserDep = Annotated[User, Depends(get_current_user)]
CurrentActiveUserDep = Annotated[User, Depends(get_current_active_user)]
AdminDep = Annotated[User, Depends(get_current_admin)]
