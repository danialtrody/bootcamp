from dataclasses import dataclass


@dataclass(frozen=True)
class Transaction:
    """
    Base class representing a financial transaction.

    Attributes:
        description (str): Short description of the transaction.
        amount (float): Positive amount of money.

    Validation:
        - description must be a non-empty string
        - amount must be a positive number
    """

    description: str
    amount: float

    def __post_init__(self) -> None:
        """Validate description and amount after initialization."""
        if not isinstance(self.description, str) or not self.description.strip():
            raise ValueError("Description must be a non-empty string")
        if not isinstance(self.amount, (int, float)) or self.amount <= 0:
            raise ValueError("Amount must be a positive number")
