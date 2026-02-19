import json
import os

READ_FROM_FILE = "r"
WRITE_TO_FILE = "w"


class JsonFileAccessor:
    """Handles reading and writing JSON data to files."""

    def __init__(self, file_path: str) -> None:
        """Initialize the accessor with a file path."""
        if file_path is None:
            raise ValueError("Please provide a legal file path")
        self.file_path = file_path

    def read(self) -> dict:
        """Read data from the JSON file."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, READ_FROM_FILE) as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}

    def write(self, data: dict) -> None:
        """Write data to the JSON file."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, WRITE_TO_FILE) as file:
            json.dump(data, file, indent=4)

    def delete(self) -> None:
        """Delete the JSON file if it exists."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def create_empty(self) -> None:
        """Create an empty JSON file with an empty dict."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, WRITE_TO_FILE) as file:
            json.dump({}, file)
