from enum import Enum
from dataclasses import dataclass
from solution.repository.base_repository import HasId


class CategoryType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass
class Category(HasId):
    name: str
    type: CategoryType
    id: int = 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value
        }
