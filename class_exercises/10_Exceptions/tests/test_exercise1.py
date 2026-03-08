from solution.exercise1 import TempFileWriter, temp_file_writer
import os
import pytest

TEST_FILE = "test.txt"
WRITE_TEXT = "Hello"


def test_class_normal_operation() -> None:
    file_name = TEST_FILE
    with TempFileWriter(file_name) as file:
        file.write(WRITE_TEXT)
        assert os.path.exists(file_name)
    assert not os.path.exists(file_name)


def test_class_exception_handling() -> None:
    file_name = TEST_FILE
    with pytest.raises(ValueError):
        with TempFileWriter(file_name) as file:
            file.write(WRITE_TEXT)
            raise ValueError("test error")
    assert not os.path.exists(file_name)


def test_class_file_writable() -> None:
    file_name = TEST_FILE
    with TempFileWriter(file_name) as file:
        file.write(WRITE_TEXT)
    assert not os.path.exists(file_name)


def test_decorator_normal_operation() -> None:
    file_name = TEST_FILE
    with temp_file_writer(file_name) as file:
        file.write(WRITE_TEXT)
        assert os.path.exists(file_name)
    assert not os.path.exists(file_name)


def test_decorator_exception_handling() -> None:
    file_name = TEST_FILE
    with pytest.raises(ValueError):
        with temp_file_writer(file_name) as file:
            file.write(WRITE_TEXT)
            raise ValueError("test error")
    assert not os.path.exists(file_name)


def test_decorator_file_writable() -> None:
    file_name = TEST_FILE
    with temp_file_writer(file_name) as file:
        file.write(WRITE_TEXT)
    assert not os.path.exists(file_name)
