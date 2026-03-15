from functools import wraps
from types import MappingProxyType
from typing import Any, Callable

from fastapi import HTTPException, status

from src.auth.exceptions import InvalidCredentialsException, NotAdminException, UserAlreadyExistsException
from src.exceptions import StudentAlreadyExistsException, StudentNotFoundException

STATUS_CODE_MAPPING: MappingProxyType[type, int] = MappingProxyType(
    {
        StudentNotFoundException: status.HTTP_404_NOT_FOUND,
        StudentAlreadyExistsException: status.HTTP_400_BAD_REQUEST,
        InvalidCredentialsException: status.HTTP_401_UNAUTHORIZED,
        NotAdminException: status.HTTP_403_FORBIDDEN,
        UserAlreadyExistsException: status.HTTP_400_BAD_REQUEST,
    }
)


def handle_exceptions() -> Callable[..., Any]:
    """Decorator factory that maps domain exceptions to HTTP responses."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except (
                StudentNotFoundException,
                StudentAlreadyExistsException,
                InvalidCredentialsException,
                NotAdminException,
                UserAlreadyExistsException,
            ) as exc:
                code = STATUS_CODE_MAPPING.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
                raise HTTPException(status_code=code, detail=str(exc))

        return wrapper

    return decorator
