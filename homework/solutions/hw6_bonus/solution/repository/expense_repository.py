from solution.business_logic.expense import Expense
from .file_accessor import JsonFileAccessor

DATA_FILE_PATH = "data/expenses.json"


class ExpenseRepository:
    """Repository for managing expense data persistence."""

    def __init__(self, file_accessor: JsonFileAccessor = None):
        self.file_accessor = file_accessor or JsonFileAccessor(DATA_FILE_PATH)

    def create(self, item: Expense) -> None:
        data = self.file_accessor.read()
        new_id = max((int(k) for k in data.keys()), default=0) + 1
        data[str(new_id)] = item.__dict__
        item._id = new_id  # internal ID for JSON
        self.file_accessor.write(data)

    def get(self, item_id: int) -> Expense:
        data = self.file_accessor.read()
        item_data = data.get(str(item_id))
        if not item_data:
            raise ValueError(f"Item with id {item_id} not found")
        expense = Expense(**item_data)
        expense._id = item_id
        return expense

    def get_all(self) -> list[Expense]:
        data = self.file_accessor.read()
        result = []
        for key, item_data in data.items():
            expense = Expense(**item_data)
            expense._id = int(key)
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
            del data[str(item_id)]
            self.file_accessor.write(data)
        else:
            raise ValueError(f"Item with id {item_id} not found")
