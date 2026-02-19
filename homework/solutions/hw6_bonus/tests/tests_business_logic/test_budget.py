from solution.business_logic.budget import Budget
from solution.business_logic.income import Income
from solution.business_logic.expense import Expense

DESCRIPTION = "description"
AMOUNT_HUNDRED = 100
AMOUNT_TWO_HUNDRED = 200
AMOUNT_NEGATIVE100 = -100


def test_create_budget_success() -> None:
    budget = Budget()
    assert budget.income == []
    assert budget.expense == []


def test_add_income() -> None:
    income = Income(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_income(income)
    assert budget.income == [income]
    assert len(budget.income) == 1


def test_add_expense() -> None:
    expense = Expense(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_expense(expense)
    assert budget.expense == [expense]
    assert len(budget.expense) == 1


def test_clear_all() -> None:
    budget = Budget()
    expense1 = Expense(DESCRIPTION, AMOUNT_HUNDRED)
    income1 = Income(DESCRIPTION, AMOUNT_HUNDRED)
    expense2 = Expense(DESCRIPTION, AMOUNT_HUNDRED)
    income2 = Income(DESCRIPTION, AMOUNT_HUNDRED)
    budget.add_expense(expense1)
    budget.add_expense(expense2)
    budget.add_income(income1)
    budget.add_income(income2)
    budget.clear_all()
    assert budget.income == []
    assert budget.expense == []
    assert len(budget.income) == 0
    assert len(budget.expense) == 0


def test_clear_all_when_already_empty() -> None:
    budget = Budget()
    budget.clear_all()
    assert budget.income == []
    assert budget.expense == []


def test_remaining_budget_zero() -> None:
    budget = Budget()
    assert budget.remaining_budget() == 0


def test_remaining_budget() -> None:
    budget = Budget()
    expense = Expense(DESCRIPTION, AMOUNT_HUNDRED)
    income = Income(DESCRIPTION, AMOUNT_TWO_HUNDRED)
    budget.add_income(income)
    budget.add_expense(expense)
    assert budget.remaining_budget() == AMOUNT_HUNDRED


def test_remaining_budget_negative() -> None:
    budget = Budget()
    expense = Expense(DESCRIPTION, AMOUNT_TWO_HUNDRED)
    income = Income(DESCRIPTION, AMOUNT_HUNDRED)
    budget.add_income(income)
    budget.add_expense(expense)
    assert budget.remaining_budget() == AMOUNT_NEGATIVE100


def test_summary_basic() -> None:
    budget = Budget()
    expense = Expense(DESCRIPTION, AMOUNT_HUNDRED)
    income = Income(DESCRIPTION, AMOUNT_TWO_HUNDRED)
    budget.add_income(income)
    budget.add_expense(expense)
    remaining_budget = AMOUNT_TWO_HUNDRED - AMOUNT_HUNDRED
    summary = budget.summary()

    assert f"  1. {DESCRIPTION}  ${AMOUNT_TWO_HUNDRED:,.2f}" in summary
    assert f"  1. {DESCRIPTION}  ${AMOUNT_HUNDRED:,.2f}" in summary
    assert f"| TOTAL INCOME: ${AMOUNT_TWO_HUNDRED:,.2f}" in summary
    assert f"| TOTAL EXPENSES: ${AMOUNT_HUNDRED:,.2f}" in summary
    assert f"| REMAINING BUDGET: ${remaining_budget:,.2f}" in summary
