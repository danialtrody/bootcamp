import pytest
from solution.business_logic.income import Income

AMOUNT_HUNDRED = 100
AMOUNT_ZERO = 0
AMOUNT_NEGATIVE = -1
DESCRIPTION = "description"
EMPTY_DESCRIPTION = ""


def test_create_income_success() -> None:
    income = Income(DESCRIPTION, AMOUNT_HUNDRED)
    assert income.description == DESCRIPTION
    assert income.amount == AMOUNT_HUNDRED


def test_create_income_zero_amount() -> None:
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        Income(DESCRIPTION, AMOUNT_ZERO)


def test_create_income_negative_amount() -> None:
    with pytest.raises(ValueError, match="Amount must be a positive number"):
        Income(DESCRIPTION, AMOUNT_NEGATIVE)


def test_create_income_empty_description() -> None:
    with pytest.raises(ValueError, match="Description must be a non-empty string"):
        Income(EMPTY_DESCRIPTION, AMOUNT_HUNDRED)
