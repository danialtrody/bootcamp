from typing import Dict, List
import os
import csv

READ_FROM_FILE = "r"
WRITE_TO_FILE = "w"
CREATE_OR_UPDATE_FILE = "a"


class CsvFileAccessor:
    def __init__(self, file_path: str):
        if file_path is None:
            raise ValueError("Provide a legal file path")

        self.file_path = file_path
        self.ensure_file_exists()

    def read(self) -> List[Dict]:
        with open(self.file_path, READ_FROM_FILE) as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        return rows

    def write(self, data: List[Dict]) -> None:
        if not data:
            raise ValueError("data is empty!")
        self.ensure_file_exists()

        with open(self.file_path, WRITE_TO_FILE, newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def ensure_file_exists(self) -> None:
        if not os.path.exists(self.file_path):
            with open(self.file_path, WRITE_TO_FILE, newline=""):
                return
