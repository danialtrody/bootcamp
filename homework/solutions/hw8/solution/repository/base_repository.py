from solution.repository.csv_accessor import CsvFileAccessor
from typing import Generic, TypeVar, Type
from dataclasses import asdict
from typing import Protocol
from dataclasses import is_dataclass


class HasId(Protocol):
    id: int


EntityType = TypeVar("EntityType", bound=HasId)


class BaseRepository(Generic[EntityType]):

    def __init__(self, accessor: CsvFileAccessor, model_type: Type[EntityType]):
        self.accessor = accessor
        self._model_type = model_type

    def create(self, item: EntityType) -> EntityType:
        if not is_dataclass(item):
            raise ValueError("Repository accepts only dataclass entities")

        data = self.accessor.read()
        data.append(asdict(item))
        self.accessor.write(data)
        return item

    def get(self, item_id: int) -> EntityType:
        data = self.accessor.read()
        for row in data:
            if str(row.get("id")) == str(item_id):
                return self._model_type(**row)
        modal_name = self._model_type.__name__
        raise ValueError(
            f"{modal_name}: Entity with ID={item_id} was not found"
        )

    def get_all(self) -> list[EntityType]:
        data = self.accessor.read()
        return [self._model_type(**row) for row in data]

    def update(self, item: EntityType) -> EntityType:
        if not is_dataclass(item):
            raise ValueError("Entity must be dataclass")

        data = self.accessor.read()
        for index, row in enumerate(data):
            if str(row.get("id")) == str(item.id):
                data[index] = asdict(item)
                self.accessor.write(data)
                return item
        modal_name = self._model_type.__name__
        raise ValueError(
            f"{modal_name}: Entity with ID={item.id} was not found"
        )

    def delete(self, item_id: int) -> None:
        data = self.accessor.read()
        for index, row in enumerate(data):
            if str(row.get("id")) == str(item_id):
                data.pop(index)
                return
        modal_name = self._model_type.__name__
        raise ValueError(
            f"{modal_name}: Entity with ID={item_id} was not found"
        )
