import pytest
from solution.business_logic.expense import Expense

AMOUNT_HUNDRED = 100
AMOUNT_ZERO = 0
AMOUNT_NEGATIVE = -1
DESCRIPTION = "description"
EMPTY_DESCRIPTION = ""


def test_create_expense_success() -> None:
    expense = Expense(DESCRIPTION, AMOUNT_HUNDRED)
    assert expense.description == DESCRIPTION
    assert expense.amount == AMOUNT_HUNDRED


def test_create_expense_invalid_amount_type() -> None:
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        Expense(DESCRIPTION, None)


def test_create_expense_invalid_description_type() -> None:
    with pytest.raises(ValueError, match="Description must be a non-empty string"):
        Expense(None, AMOUNT_HUNDRED)


def test_create_expense_zero_amount() -> None:
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        Expense(DESCRIPTION, AMOUNT_ZERO)


def test_create_expense_negative_amount() -> None:
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        Expense(DESCRIPTION, AMOUNT_NEGATIVE)


def test_create_expense_empty_description() -> None:
    with pytest.raises(ValueError, match="Description must be a non-empty string"):
        Expense(EMPTY_DESCRIPTION, AMOUNT_HUNDRED)
