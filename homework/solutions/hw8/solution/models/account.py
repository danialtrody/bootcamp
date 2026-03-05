from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Account:
    id: int
    name: str
    opening_balance: Decimal
