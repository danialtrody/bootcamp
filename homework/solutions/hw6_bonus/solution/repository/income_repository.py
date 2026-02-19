from typing import cast
from solution.business_logic.income import Income
from .file_accessor import JsonFileAccessor
from solution.business_logic.protocols import HasID

DATA_FILE_PATH = "data/incomes.json"


class IncomeRepository:
    """Repository for managing income data persistence."""

    def __init__(self, file_accessor: JsonFileAccessor | None = None):
        self.file_accessor = file_accessor or JsonFileAccessor(DATA_FILE_PATH)

    def create(self, item: Income) -> None:
        data = self.file_accessor.read()
        new_id = max((int(key) for key in data.keys()), default=0) + 1
        data[str(new_id)] = item.__dict__
        cast(HasID, item)._id = new_id
        self.file_accessor.write(data)

    def get(self, item_id: int) -> Income:
        data = self.file_accessor.read()
        item_data = data.get(str(item_id))
        if not item_data:
            raise ValueError(f"Item with id {item_id} not found")
        income = Income(**item_data)
        cast(HasID, income)._id = item_id
        return income

    def get_all(self) -> list[Income]:
        data = self.file_accessor.read()
        result: list[Income] = []
        for key, item_data in data.items():
            item_data = dict(item_data)
            item_data.pop("_id", None)
            income = Income(**item_data)
            cast(HasID, income)._id = int(key)
            result.append(income)
        return result

    def update(self, item_id: int, item: Income) -> None:
        data = self.file_accessor.read()
        key = str(item_id)
        if key not in data:
            raise ValueError(f"Item with id {item_id} not found")
        data[key] = item.__dict__
        self.file_accessor.write(data)

    def delete(self, item_id: int) -> None:
        data = self.file_accessor.read()
        if str(item_id) in data:
            data.pop(str(item_id), None)
            self.file_accessor.write(data)
        else:
            raise ValueError(f"Item with id {item_id} not found")
