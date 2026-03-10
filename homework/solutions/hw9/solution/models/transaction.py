from dataclasses import dataclass
from decimal import Decimal
from solution.repository.base_repository import HasId
import datetime


@dataclass
class Transaction(HasId):
    amount: Decimal
    date: datetime.date
    type: str
    account_id: int
    category_id: int
    id: int = 0
