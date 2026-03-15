class StudentNotFoundException(Exception):
    """Raised when a student does not exist."""


class StudentAlreadyExistsException(Exception):
    """Raised when creating a student with a duplicate email."""
