from solution.repository.csv_accessor import CsvFileAccessor
from typing import Generic, TypeVar, Type
from typing import Protocol
from typing import Dict, Any
from dataclasses import is_dataclass
from dataclasses import fields
from decimal import Decimal
import datetime
from enum import Enum


ID = "id"


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
        max_id = max([int(row.get(ID, 0)) for row in data], default=0)
        item.id = max_id + 1

        data.append(self._serialize_item(item))
        self.accessor.write(data)
        return item

    def get(self, item_id: int) -> EntityType:
        data = self.accessor.read()
        for row in data:
            if str(row.get(ID)) == str(item_id):
                deserialized = self._deserialize_row(row)
                return self._model_type(**deserialized)
        modal_name = self._model_type.__name__
        raise ValueError(f"{modal_name}: Entity with ID={item_id} was not found")

    def get_all(self) -> list[EntityType]:
        data = self.accessor.read()
        return [self._model_type(**self._deserialize_row(row)) for row in data]

    def update(self, item: EntityType) -> EntityType:
        if not is_dataclass(item):
            raise ValueError("Entity must be dataclass")

        data = self.accessor.read()
        for index, row in enumerate(data):
            if str(row.get("id")) == str(item.id):
                data[index] = self._serialize_item(item)
                self.accessor.write(data)
                return item
        modal_name = self._model_type.__name__
        raise ValueError(f"{modal_name}: Entity with ID={item.id} was not found")

    def delete(self, item_id: int) -> None:
        data = self.accessor.read()
        for index, row in enumerate(data):
            if str(row.get("id")) == str(item_id):
                data.pop(index)
                self.accessor.write(data)
                return
        modal_name = self._model_type.__name__
        raise ValueError(f"{modal_name}: Entity with ID={item_id} was not found")

    def _serialize_item(self, item: EntityType) -> Dict[str, Any]:
        result: Dict[str, Any] = {}

        if not is_dataclass(item):
            raise ValueError("Item must be dataclass instance")
        for field in fields(item):
            value = getattr(item, field.name)
            result[field.name] = self._convert_serialize_value(value)

        return result

    def _deserialize_row(self, row: dict) -> Dict[str, Any]:
        result: Dict[str, Any] = {}

        if not is_dataclass(self._model_type):
            raise ValueError("Model type must be dataclass")

        for field in fields(self._model_type):
            raw_value = row.get(field.name)
            if raw_value in (None, ""):
                result[field.name] = None
                continue
            try:
                result[field.name] = self._convert_deserialize_value(
                    field.type, raw_value
                )
            except Exception:
                result[field.name] = raw_value

        return result

    def _convert_deserialize_value(self, field_type: Any, value: Any) -> Any:

        if field_type == int:
            return int(value)
        if field_type == Decimal:
            return Decimal(str(value))
        if field_type == datetime.date:
            return datetime.date.fromisoformat(value)
        if isinstance(field_type, type) and issubclass(field_type, Enum):
            return field_type(value)

        return value

    def _convert_serialize_value(self, value: Any) -> Any:
        if value is None:
            return ""
        if isinstance(value, Decimal):
            return str(value)
        if isinstance(value, datetime.date):
            return value.isoformat()
        if isinstance(value, Enum):
            return value.value

        return value
