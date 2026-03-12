from dataclasses import dataclass
from decimal import Decimal
import datetime
from solution.repository.base_repository import HasId


@dataclass
class Transfer(HasId):
    amount: Decimal
    date: datetime.date
    description: str
    from_account_id: int
    to_account_id: int
    id: int = 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "amount": self.amount,
            "date": self.date.isoformat(),
            "description": self.description,
            "from_account_id": self.from_account_id,
            "to_account_id": self.to_account_id,
        }
