import json
import pytest
from pathlib import Path
from solution.repository.file_accessor import JsonFileAccessor

TEST_FILE_NAME = "test_data.json"
WRONG_FILE_NAME = "not_exists.json"
NEW_FILE_JSON = "new_file.json"


def json_content() -> dict[str, object]:
    return {"key": "value", "number": 42}


@pytest.fixture
def prepared_json_file(tmp_path: Path) -> Path:
    """Fixture to prepare a JSON file for testing."""
    file_path = tmp_path / TEST_FILE_NAME
    with open(file_path, "w") as file:
        json.dump(json_content(), file)
    return file_path


def test_read(prepared_json_file: Path) -> None:
    file_path = str(prepared_json_file)
    accessor = JsonFileAccessor(file_path)
    content = accessor.read()
    assert content == json_content()


def test_write(prepared_json_file: Path) -> None:
    file_path = str(prepared_json_file)
    accessor = JsonFileAccessor(file_path)
    new_content = {"new": "data", "num": 123}

    accessor.write(new_content)

    with open(file_path, "r") as file:
        content = json.load(file)

    assert content == new_content


def test_read_non_existing_file(tmp_path: Path) -> None:
    file_path = tmp_path / WRONG_FILE_NAME
    accessor = JsonFileAccessor(str(file_path))

    content = accessor.read()

    assert content == {}


def test_write_non_existing_file(tmp_path: Path) -> None:
    file_path = tmp_path / NEW_FILE_JSON
    accessor = JsonFileAccessor(str(file_path))
    new_content = {"new": "data", "num": 123}

    accessor.write(new_content)

    with open(file_path, "r") as file:
        content = json.load(file)

    assert content == new_content
