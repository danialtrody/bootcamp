import os
import csv
import pytest
from pathlib import Path
from typing import Dict, List
from solution.repository.csv_accessor import CsvFileAccessor

READ_FROM_FILE = "r"
WRITE_TO_FILE = "w"


def test_creates_file_if_not_exists(tmp_path: Path) -> None:
    file_path = tmp_path / "test.csv"
    CsvFileAccessor(str(file_path))
    assert os.path.exists(file_path)


@pytest.mark.parametrize(
    "data, success_output",
    [
        ([{"id": 1}], [{"id": "1"}]),
        ([{"id": 1, "name": "test"}], [{"id": "1", "name": "test"}]),
    ],
)
def test_write_success(
    tmp_path: Path, data: List[Dict], success_output: List[Dict]
) -> None:
    file_path = tmp_path / "test.csv"
    csv_file_accessor = CsvFileAccessor(str(file_path))
    csv_file_accessor.write(data)

    with open(file_path, READ_FROM_FILE) as file:
        reader = csv.DictReader(file)
        rows = list(reader)

        assert reader.fieldnames == list(data[0].keys())

    assert rows == success_output
    assert len(rows) == len(success_output)


def test_write_fail(tmp_path: Path) -> None:
    file_path = tmp_path / "test.csv"
    csv_file_accessor = CsvFileAccessor(str(file_path))

    with pytest.raises(ValueError, match="data is empty!"):
        csv_file_accessor.write([])


@pytest.mark.parametrize(
    "data, output",
    [
        ([{"id": 1}], [{"id": "1"}]),
        ([{"id": 1, "name": "test"}], [{"id": "1", "name": "test"}]),
    ],
)
def test_read(tmp_path: Path, data: List[Dict], output: List[Dict]) -> None:

    file_path = tmp_path / "test.csv"
    csv_file_accessor = CsvFileAccessor(str(file_path))

    with open(file_path, WRITE_TO_FILE, newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    content = csv_file_accessor.read()

    assert content == output
    assert len(content) == len(output)


def test_read_empty_file(tmp_path: Path) -> None:

    file_path = tmp_path / "test.csv"
    csv_file_accessor = CsvFileAccessor(str(file_path))

    content = csv_file_accessor.read()

    assert content == []
    assert len(content) == 0
