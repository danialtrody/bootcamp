from typing import cast
from solution.business_logic.expense import Expense
from .file_accessor import JsonFileAccessor
from solution.business_logic.protocols import HasID

DATA_FILE_PATH = "data/expenses.json"


class ExpenseRepository:
    """Repository for managing expense data persistence."""

    def __init__(self, file_accessor: JsonFileAccessor | None = None):
        self.file_accessor = file_accessor or JsonFileAccessor(DATA_FILE_PATH)

    def create(self, item: Expense) -> None:
        data = self.file_accessor.read()
        new_id = max((int(key) for key in data.keys()), default=0) + 1
        data[str(new_id)] = item.__dict__
        cast(HasID, item)._id = new_id  # <-- cast ל־Protocol
        self.file_accessor.write(data)

    def get(self, item_id: int) -> Expense:
        data = self.file_accessor.read()
        item_data = data.get(str(item_id))
        if not item_data:
            raise ValueError(f"Item with id {item_id} not found")
        expense = Expense(**item_data)
        cast(HasID, expense)._id = item_id  # <-- cast ל־Protocol
        return expense

    def get_all(self) -> list[Expense]:
        data = self.file_accessor.read()
        result: list[Expense] = []
        for key, item_data in data.items():
            expense = Expense(**item_data)
            cast(HasID, expense)._id = int(key)  # <-- cast ל־Protocol
            result.append(expense)
        return result

    def update(self, item_id: int, item: Expense) -> None:
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
