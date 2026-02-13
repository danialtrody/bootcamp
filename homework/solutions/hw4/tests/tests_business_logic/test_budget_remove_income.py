import pytest
from solution.business_logic.budget import Budget
from solution.business_logic.income import Income

DESCRIPTION = "description"
WRONGDESCRIPTION = "wrong"
INDEX_ZERO = 0
INDEX_ONE = 1
AMOUNT_HUNDRED = 100


def test_remove_income_by_description_success() -> None:
    income = Income(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_income(income)
    budget.remove_income(DESCRIPTION)
    assert budget.income == []
    assert len(budget.income) == 0


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


def test_remove_income_by_index_success() -> None:
    income = Income(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_income(income)
    budget.remove_income(INDEX_ONE)
    assert budget.income == []
    assert len(budget.income) == 0


def test_remove_income_by_index_failed() -> None:
    income = Income(DESCRIPTION, AMOUNT_HUNDRED)
    budget = Budget()
    budget.add_income(income)
    income_length = len(budget.income)
    expected_output = (
        f"Invalid index {INDEX_ZERO}. Index must be between 1 and {income_length}."
    )
    with pytest.raises(IndexError, match=expected_output):
        budget.remove_income(INDEX_ZERO)


def test_remove_income_by_index_empty_list_failed() -> None:
    budget = Budget()
    expected_output = "Cannot remove income: the income list is empty."
    with pytest.raises(ValueError, match=expected_output):
        budget.remove_income(INDEX_ZERO)


def test_remove_income_by_desc_empty_list_fail() -> None:
    budget = Budget()
    expected_output = "Cannot remove income: the income list is empty."
    with pytest.raises(ValueError, match=expected_output):
        budget.remove_income(DESCRIPTION)
