from dataclasses import dataclass
from decimal import Decimal
from solution.repository.base_repository import HasId
import datetime
from typing import Any


@dataclass
class Transaction(HasId):
    amount: Decimal
    date: datetime.date
    type: str
    account_id: int
    category_id: int
    id: int = 0

    def to_dict(self) -> dict[str, Any]:
        if isinstance(self.date, str):
            date_str = self.date
        else:
            date_str = self.date.isoformat()
        return {
            "id": self.id,
            "amount": float(self.amount),
            "date": date_str,
            "type": self.type,
            "account_id": self.account_id,
            "category_id": self.category_id,
        }
