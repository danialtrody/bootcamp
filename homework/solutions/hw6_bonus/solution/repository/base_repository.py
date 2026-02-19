from abc import ABC, abstractmethod
from solution.repository.file_accessor import JsonFileAccessor


class BaseRepository(ABC):
    """Base repository with common CRUD operations."""

    def __init__(self, file_accessor: JsonFileAccessor):
        self.file_accessor = file_accessor

    def _read_data(self) -> dict:
        return self.file_accessor.read()

    def _write_data(self, data: dict) -> None:
        self.file_accessor.write(data)

    @abstractmethod
    def create(self, item):
        pass

    @abstractmethod
    def get(self, item_id: int):
        pass

    @abstractmethod
    def get_all(self) -> list:
        pass

    @abstractmethod
    def update(self, item_id: int, item) -> None:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> None:
        pass
