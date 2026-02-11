"""Budget module - defines the Budget class for managing incomes and expenses."""

from solution.business_logic.expense import Expense
from solution.business_logic.income import Income
from typing import List


class Budget:
    """Manage incomes and expenses."""

    def __init__(self) -> None:
        """Initialize empty income and expense lists."""
        self._income: List[Income] = []
        self._expense: List[Expense] = []

    @property
    def income(self) -> List[Income]:
        return self._income

    @property
    def expense(self) -> List[Expense]:
        return self._expense

    # ====================== Public Methods ======================

    def add_income(self, income: Income) -> None:
        """Add an Income object."""
        if not isinstance(income, Income):
            raise TypeError("Expected Income instance")
        self._income.append(income)

    def add_expense(self, expense: Expense) -> None:
        """Add an Expense object."""
        if not isinstance(expense, Expense):
            raise TypeError("Expected Expense instance")
        self._expense.append(expense)

    def remove_income(self, description_or_index: str | int) -> None:
        """Remove an income by description or index."""
        if len(self.income) == 0:
            raise ValueError("Cannot remove income: the income list is empty.")
        self._remove_item(self._income, description_or_index)

    def remove_expense(self, description_or_index: str | int) -> None:
        """Remove an expense by description or index."""
        if len(self.expense) == 0:
            raise ValueError("Cannot remove expense: the expense list is empty.")
        self._remove_item(self._expense, description_or_index)

    def clear_all(self) -> None:
        """Clear all incomes and expenses."""
        self._expense.clear()
        self._income.clear()

    def total_income(self) -> float:
        """Return total income amount."""
        return sum(item.amount for item in self.income)

    def total_expense(self) -> float:
        """Return total expense amount."""
        return sum(item.amount for item in self.expense)

    def remaining_budget(self) -> float:
        """Return remaining budget (income - expenses)."""
        return self.total_income() - self.total_expense()

    def summary(self) -> str:
        """Return a summary of incomes, expenses, and remaining budget."""
        income_lines = "\n".join(
            f"{income.description}: {income.amount}" for income in self.income
        )
        total_income = sum(income.amount for income in self.income)

        expense_lines = "\n".join(
            f"{expense.description}: {expense.amount}" for expense in self.expense
        )
        total_expense = sum(expense.amount for expense in self.expense)

        remaining_budget = total_income - total_expense

        result = (
            f"Income:\n{income_lines}\n"
            f"Total Income: {total_income}\n\n"
            f"Expenses:\n{expense_lines}\n"
            f"Total Expenses: {total_expense}\n\n"
            f"Remaining Budget: {remaining_budget}"
        )

        return result

    # ======================  helper private methods ======================

    def _remove_item(self, lst: list, description_or_index: str | int) -> None:
        """Remove item from list by description or index."""
        if not lst:
            raise ValueError(f"Cannot remove {description_or_index}: list is empty")
        if isinstance(description_or_index, str):
            self._remove_item_by_description(lst, description_or_index)
        elif isinstance(description_or_index, int):
            self._remove_item_by_index(lst, description_or_index)
        else:
            raise TypeError("Argument must be int (index) or str (description)")

    def _remove_item_by_description(self, lst: list, description_or_index: str) -> None:
        """Remove first item in list matching description."""
        item_type = "income" if lst is self._income else "expense"
        for item in lst:
            if item.description == description_or_index:
                lst.remove(item)
                return
        raise ValueError(
            f"No {item_type} found with description '{description_or_index}'. "
            f"Please make sure the description matches an existing {item_type}."
        )

    def _remove_item_by_index(self, lst: list, description_or_index: int) -> None:
        """Remove item in list by index."""
        if not (0 <= description_or_index < len(lst)):
            list_length = len(lst) - 1
            raise IndexError(
                f"Invalid index {description_or_index}. "
                f"Index must be between 0 and {list_length}."
            )
        lst.pop(description_or_index)
