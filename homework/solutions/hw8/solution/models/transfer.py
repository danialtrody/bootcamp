from dataclasses import dataclass
from decimal import Decimal
import datetime


@dataclass
class Transfer:
    id: int
    amount: Decimal
    date: datetime.date
    description: str
    from_account_id: int
    to_account_id: int
