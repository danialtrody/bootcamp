from pathlib import Path
from solution.repository.file_accessor import JsonFileAccessor


def test_write_and_read(tmp_path: Path) -> None:
    file_path = tmp_path / "test.json"
    accessor = JsonFileAccessor(str(file_path))

    data = {"name": "Danial", "age": 25}
    accessor.write(data)

    read_data = accessor.read()
    assert read_data == data
