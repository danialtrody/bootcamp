from dataclasses import dataclass
from decimal import Decimal
import datetime
from solution.repository.base_repository import HasId


@dataclass
class Transfer(HasId):
    id: int
    amount: Decimal
    date: datetime.date
    description: str
    from_account_id: int
    to_account_id: int
