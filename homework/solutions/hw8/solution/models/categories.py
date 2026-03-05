from enum import Enum
from dataclasses import dataclass


class CategoryType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass
class Category:
    id: int
    name: str
    type: CategoryType
