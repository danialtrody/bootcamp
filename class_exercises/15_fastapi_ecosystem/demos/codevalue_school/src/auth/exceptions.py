class BearAuthException(Exception):
    """Raised when a JWT token cannot be validated."""


class AuthSessionExpiredException(Exception):
    """Raised when the session or JWT token has expired."""


class InvalidCredentialsException(Exception):
    """Raised when email or password is incorrect."""


class NotAdminException(Exception):
    """Raised when a non-admin user attempts to access admin-only resources."""


class UserAlreadyExistsException(Exception):
    """Raised when registering with an email that already exists."""
