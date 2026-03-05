from dataclasses import dataclass
from decimal import Decimal
import datetime


@dataclass
class Transaction:
    id: int
    amount: Decimal
    date: datetime.date
    type: str
    account_id: int
    category_id: int
