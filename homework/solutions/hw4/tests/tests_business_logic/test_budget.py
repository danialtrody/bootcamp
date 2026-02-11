import pytest
from solution.business_logic.budget import Budget
from solution.business_logic.income import Income
from solution.business_logic.expense import Expense

DESCRIPTION = "description"
WRONGDESCRIPTION = "wrong"
INDEX_ZERO = 0
INDEX_ONE = 1
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


def test_remove_income_by_description_success() -> None:
    income = Income(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_income(income)
    budget.remove_income(DESCRIPTION)
    assert budget.income == []
    assert len(budget.income) == 0


def test_remove_expense_by_description_success() -> None:
    expense = Expense(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_expense(expense)
    budget.remove_expense(DESCRIPTION)
    assert budget.expense == []
    assert len(budget.expense) == 0


def test_remove_income_by_description_failed() -> None:
    income = Income(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_income(income)
    expected_output = (
        f"No income found with description '{WRONGDESCRIPTION}'. "
        f"Please make sure the description matches an existing income."
    )
    with pytest.raises(ValueError, match=expected_output):
        budget.remove_income(WRONGDESCRIPTION)


def test_remove_expense_by_description_failed() -> None:
    expense = Expense(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_expense(expense)
    expected_output = (
        f"No expense found with description '{WRONGDESCRIPTION}'. "
        f"Please make sure the description matches an existing expense."
    )
    with pytest.raises(ValueError, match=expected_output):
        budget.remove_expense(WRONGDESCRIPTION)


def test_remove_income_by_index_success() -> None:
    income = Income(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_income(income)
    budget.remove_income(INDEX_ZERO)
    assert budget.income == []
    assert len(budget.income) == 0


def test_remove_expense_by_index_success() -> None:
    expense = Expense(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_expense(expense)
    budget.remove_expense(INDEX_ZERO)
    assert budget.expense == []
    assert len(budget.expense) == 0


def test_remove_income_by_index_failed() -> None:
    income = Income(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_income(income)
    income_length = len(budget.income) - 1
    expected_output = (
        f"Invalid index {INDEX_ONE}. Index must be between 0 and {income_length}."
    )
    with pytest.raises(IndexError, match=expected_output):
        budget.remove_income(INDEX_ONE)


def test_remove_expense_by_index_failed() -> None:
    expense = Expense(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_expense(expense)
    expense_length = len(budget.expense) - 1
    expected_output = (
        f"Invalid index {INDEX_ONE}. Index must be between 0 and {expense_length}."
    )
    with pytest.raises(IndexError, match=expected_output):
        budget.remove_expense(INDEX_ONE)


def test_remove_income_by_index_empty_list_failed() -> None:
    budget = Budget()
    expected_output = "Cannot remove income: the income list is empty."
    with pytest.raises(ValueError, match=expected_output):
        budget.remove_income(INDEX_ZERO)


def test_remove_expense_by_index_empty_list_fail() -> None:
    budget = Budget()
    expected_output = "Cannot remove expense: the expense list is empty."
    with pytest.raises(ValueError, match=expected_output):
        budget.remove_expense(INDEX_ZERO)


def test_remove_income_by_desc_empty_list_fail() -> None:
    budget = Budget()
    expected_output = "Cannot remove income: the income list is empty."
    with pytest.raises(ValueError, match=expected_output):
        budget.remove_income(DESCRIPTION)


def test_remove_expense_by_desc_empty_list_fail() -> None:
    budget = Budget()
    expected_output = "Cannot remove expense: the expense list is empty."
    with pytest.raises(ValueError, match=expected_output):
        budget.remove_expense(DESCRIPTION)


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


def test_total_income_empty_lists() -> None:
    budget = Budget()
    assert budget.total_income() == 0


def test_total_expense_empty_lists() -> None:
    budget = Budget()
    assert budget.total_expense() == 0


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
    assert f"{DESCRIPTION}: {AMOUNT_TWO_HUNDRED}" in summary
    assert f"{DESCRIPTION}: {AMOUNT_HUNDRED}" in summary
    assert f"Total Income: {AMOUNT_TWO_HUNDRED}" in summary
    assert f"Total Expenses: {AMOUNT_HUNDRED}" in summary
    assert f"Remaining Budget: {remaining_budget}" in summary
