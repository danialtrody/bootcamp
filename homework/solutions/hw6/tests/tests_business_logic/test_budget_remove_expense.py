import pytest
from solution.business_logic.budget import Budget
from solution.business_logic.expense import Expense

DESCRIPTION = "description"
WRONGDESCRIPTION = "wrong"
INDEX_ZERO = 0
INDEX_ONE = 1
AMOUNT_HUNDRED = 100


def test_remove_expense_by_description_success() -> None:
    expense = Expense(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_expense(expense)
    budget.remove_expense(DESCRIPTION)
    assert budget.expense == []
    assert len(budget.expense) == 0


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


def test_remove_expense_by_index_success() -> None:
    expense = Expense(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_expense(expense)
    budget.remove_expense(INDEX_ONE)
    assert budget.expense == []
    assert len(budget.expense) == 0


def test_remove_expense_by_index_failed() -> None:
    expense = Expense(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_expense(expense)
    expense_length = len(budget.expense)
    expected_output = (
        f"Invalid index {INDEX_ZERO}. Index must be between 1 and {expense_length}."
    )
    with pytest.raises(IndexError, match=expected_output):
        budget.remove_expense(INDEX_ZERO)


def test_remove_expense_by_index_empty_list_fail() -> None:
    budget = Budget()
    expected_output = "Cannot remove expense: the expense list is empty."
    with pytest.raises(ValueError, match=expected_output):
        budget.remove_expense(INDEX_ZERO)


def test_remove_expense_by_desc_empty_list_fail() -> None:
    budget = Budget()
    expected_output = "Cannot remove expense: the expense list is empty."
    with pytest.raises(ValueError, match=expected_output):
        budget.remove_expense(DESCRIPTION)
