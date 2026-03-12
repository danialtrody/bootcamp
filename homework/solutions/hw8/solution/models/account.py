from dataclasses import dataclass
from decimal import Decimal
from solution.repository.base_repository import HasId


@dataclass
class Account(HasId):
    id: int = 0
    name: str = ""
    opening_balance: Decimal = Decimal("0")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "opening_balance": self.opening_balance
        }
