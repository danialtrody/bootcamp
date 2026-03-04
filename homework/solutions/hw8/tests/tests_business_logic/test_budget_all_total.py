from solution.business_logic.budget import Budget
from solution.business_logic.income import Income
from solution.business_logic.expense import Expense

DESCRIPTION = "description"
AMOUNT_HUNDRED = 100


def test_total_expense_empty_lists() -> None:
    budget = Budget()
    assert budget.total_expense() == 0


def test_total_income_empty_lists() -> None:
    budget = Budget()
    assert budget.total_income() == 0


def test_total_income() -> None:
    budget = Budget()
    income1 = Income(DESCRIPTION, AMOUNT_HUNDRED)
    income2 = Income(DESCRIPTION, AMOUNT_HUNDRED)
    budget.add_income(income1)
    budget.add_income(income2)
    assert budget.total_income() == AMOUNT_HUNDRED + AMOUNT_HUNDRED


def test_total_expense() -> None:
    budget = Budget()
    expense1 = Expense(DESCRIPTION, AMOUNT_HUNDRED)
    expense2 = Expense(DESCRIPTION, AMOUNT_HUNDRED)
    budget.add_expense(expense1)
    budget.add_expense(expense2)
    assert budget.total_expense() == AMOUNT_HUNDRED + AMOUNT_HUNDRED
