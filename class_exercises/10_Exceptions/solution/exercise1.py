from contextlib import contextmanager
from typing import Iterator, TextIO, Optional
import os


class TempFileWriter:

    def __init__(self, file_name: str) -> None:
        if file_name is None:
            raise ValueError("Please provide a legal file name")

        self.file_name = file_name
        self.file = None

    def __enter__(self) -> TextIO:
        self.file = open(self.file_name, "w")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.file:
            self.file.close()
        os.remove(self.file_name)


@contextmanager
def temp_file_writer(file_name: str):
    file = open(file_name, "w")

    try:
        yield file
    finally:
        file.close()
        os.remove(file_name)
