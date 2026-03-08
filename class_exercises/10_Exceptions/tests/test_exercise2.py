import pytest
import os
from solution.exercise2 import (
    parse_config,
    ConfigFileNotFoundError,
    ConfigParseError,
    ConfigValidationError,
)

FIRST_KEY: str = "KEY1"
SECOND_KEY: str = "KEY2"


def create_temp_file(filename: str, content: str) -> None:
    """Creates a temporary file with the given content."""
    with open(filename, "w") as file:
        file.write(content)


def remove_temp_file(filename: str) -> None:
    """Removes the temporary file if it exists."""
    if os.path.exists(filename):
        os.remove(filename)


def test_successful_parsing() -> None:
    filename: str = "test_successful.txt"
    content: str = """
    # This is a comment
    KEY1=VALUE1
    KEY2=VALUE2
    """
    create_temp_file(filename, content)

    result: dict[str, str] = parse_config(filename, [FIRST_KEY, SECOND_KEY])
    assert result == {FIRST_KEY: "VALUE1", SECOND_KEY: "VALUE2"}

    remove_temp_file(filename)


def test_file_not_found() -> None:
    filename: str = "nonexistent.txt"
    with pytest.raises(ConfigFileNotFoundError):
        parse_config(filename, [FIRST_KEY, SECOND_KEY])


def test_parse_error() -> None:
    filename: str = "temp_invalid.cfg"
    content: str = """
    invalid_line_without_equals
    TEST=TEST
    """
    create_temp_file(filename, content)

    with pytest.raises(ConfigParseError):
        parse_config(filename, ["TEST"])

    remove_temp_file(filename)


def test_validation_error_missing_key() -> None:
    filename: str = "test_missing_key.txt"
    content: str = """
    KEY1=VALUE1
    """
    create_temp_file(filename, content)

    with pytest.raises(ConfigValidationError):
        parse_config(filename, [FIRST_KEY, SECOND_KEY])

    remove_temp_file(filename)
