"""Income module - defines the Income class for Budget Planner."""


class Income:
    """Represents an income with a description and a positive amount."""

    def __init__(self, description: str, amount: float) -> None:
        """Create Income. Raises ValueError if amount <= 0 or description is empty."""

        if not isinstance(description, str) or description.strip() == "":
            raise ValueError("Description must be a non-empty string")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number")

        self._description = description
        self._amount = amount

    @property
    def description(self) -> str:
        return self._description

    @property
    def amount(self) -> float:
        return self._amount

    def __repr__(self) -> str:
        return f"Income(description={self.description}, amount={self.amount})"

    def __str__(self) -> str:
        return f"{self.description}: {self.amount:,.2f}"
