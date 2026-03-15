from enum import Enum

SESSION_EXPIRY_HOURS = 8
JWT_EXPIRATION_SECONDS = 1800
TOKEN_REFRESH_THRESHOLD = 300


class UserRole(Enum):
    ADMIN = "admin"
    STUDENT = "student"

    @classmethod
    def values(cls) -> list[str]:
        return [role.value for role in cls]
