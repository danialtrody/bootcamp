"""Budget module - defines the Budget class for managing incomes and expenses."""

from solution.business_logic.expense import Expense
from solution.business_logic.income import Income
from typing import List, Protocol


class _BudgetProtocol(Protocol):
    """Protocol that defines required Budget interface for helper methods."""

    @property
    def income(self) -> List[Income]:
        ...

    @property
    def expense(self) -> List[Expense]:
        ...

    def total_income(self) -> float:
        ...

    def total_expense(self) -> float:
        ...

    def remaining_budget(self) -> float:
        ...


class _BudgetHelper:
    """Helper class for removing items from lists."""

    def remaining_budget(self: _BudgetProtocol) -> float:
        """Return remaining budget (income - expenses)."""
        return self.total_income() - self.total_expense()

    def summary(self: _BudgetProtocol) -> str:
        """Return a nicely formatted summary of incomes, expenses, and remaining budget."""

        income_lines = "\n".join(
            f"  {index}. {income.description}  ${income.amount:,.2f}"
            for index, income in enumerate(self.income, start=1)
        ) + "\n"

        expense_lines = "\n".join(
            f"  {index}. {expense.description:}  ${expense.amount:,.2f}"
            for index, expense in enumerate(self.expense, start=1)
        ) + "\n"

        total_income = self.total_income()
        total_expense = self.total_expense()
        remaining_budget = self.remaining_budget()

        return (
            "\n|====================================|\n"
            "|           BUDGET SUMMARY           |\n"
            "|====================================|\n"
            "|                                    |\n"
            "| INCOME SOURCES:                    |\n"
            f"{income_lines}"
            "|------------------------------------|\n"
            f"| TOTAL INCOME: ${total_income:,.2f}\n"
            "|                                    |\n"
            "| EXPENSES:                          |\n"
            f"{expense_lines}"
            "|------------------------------------|\n"
            f"| TOTAL EXPENSES: ${total_expense:,.2f}\n"
            "|                                    |\n"
            "|====================================|\n"
            f"| REMAINING BUDGET: ${remaining_budget:,.2f}\n"
            "|====================================|\n"
        )

    def remove_item(
        self, lst: List[Income] | List[Expense], description_or_index: str | int
    ) -> None:
        """Remove item from list by description or index."""

        if isinstance(description_or_index, str):
            self._remove_item_by_description(lst, description_or_index)
        elif isinstance(description_or_index, int):
            self._remove_item_by_index(lst, description_or_index)
        else:
            raise TypeError("Argument must be int (index) or str (description)")

    def _remove_item_by_description(self, lst: list, description_or_index: str) -> None:
        """Remove first item in list matching description."""
        item_type = "income" if lst and isinstance(lst[0], Income) else "expense"
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


class Budget(_BudgetHelper):
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
        self.remove_item(self._income, description_or_index)

    def remove_expense(self, description_or_index: str | int) -> None:
        """Remove an expense by description or index."""
        if len(self.expense) == 0:
            raise ValueError("Cannot remove expense: the expense list is empty.")
        self.remove_item(self._expense, description_or_index)

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
