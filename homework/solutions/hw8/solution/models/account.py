from typing import Optional
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Account:
    id: Optional[int] = None
    name: str = ""
    opening_balance: Decimal = Decimal("0")
