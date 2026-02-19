from abc import ABC, abstractmethod
from solution.repository.file_accessor import JsonFileAccessor
from typing import Any, Optional


class BaseRepository(ABC):
    """Base repository with common CRUD operations."""

    def __init__(self, file_accessor: JsonFileAccessor):
        self.file_accessor = file_accessor

    @abstractmethod
    def create(self, item: Any) -> None:
        ...

    @abstractmethod
    def get(self, item_id: int) -> Optional[Any]:
        ...

    @abstractmethod
    def get_all(self) -> list[Any]:
        ...

    @abstractmethod
    def update(self, item_id: int, item: Any) -> None:
        ...

    @abstractmethod
    def delete(self, item_id: int) -> None:
        ...

    def _read_data(self) -> dict:
        return self.file_accessor.read()

    def _write_data(self, data: dict) -> None:
        self.file_accessor.write(data)
