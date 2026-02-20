import pytest
from unittest.mock import MagicMock
from solution.repository.expense_repository import ExpenseRepository
from solution.business_logic.expense import Expense


FOOD = "Food"
FOOD_ONE = "Food_one"
FOOD_TWO = "Food_two"
TEST_VALUE = "TEST"
UPDATED_TEST = "Updated TEST"
EXPENSE_VALUE = "Expense"

ID_ONE = "1"
ID_TWO = "2"

DESCRIPTION = "description"
AMOUNT = "amount"


@pytest.fixture
def mock_accessor() -> MagicMock:
    mock = MagicMock()
    mock.read.return_value = {}
    return mock


def test_create_expense(mock_accessor: MagicMock) -> None:
    repository = ExpenseRepository(file_accessor=mock_accessor)
    expense = Expense(FOOD, 1000)

    repository.create(expense)

    mock_accessor.read.assert_called_once()
    mock_accessor.write.assert_called_once()

    written_data = mock_accessor.write.call_args[0][0]

    assert ID_ONE in written_data
    assert written_data[ID_ONE][DESCRIPTION] == FOOD
    assert written_data[ID_ONE][AMOUNT] == 1000


def test_get_expense(mock_accessor: MagicMock) -> None:
    mock_accessor.read.return_value = {
        ID_ONE: {DESCRIPTION: FOOD, AMOUNT: 1000},
    }
    repository = ExpenseRepository(file_accessor=mock_accessor)

    expense = repository.get(1)

    assert expense.description == FOOD
    assert expense.amount == 1000


def test_get_all_expense(mock_accessor: MagicMock) -> None:
    mock_accessor.read.return_value = {
        ID_ONE: {DESCRIPTION: FOOD_ONE, AMOUNT: 1000},
        ID_TWO: {DESCRIPTION: FOOD_TWO, AMOUNT: 2000},
    }
    repository = ExpenseRepository(file_accessor=mock_accessor)

    expense = repository.get_all()

    assert len(expense) == 2
    assert expense[0].description == FOOD_ONE
    assert expense[0].amount == 1000
    assert expense[1].description == FOOD_TWO
    assert expense[1].amount == 2000


def test_update_expense(mock_accessor: MagicMock) -> None:
    mock_accessor.read.return_value = {
        ID_ONE: {DESCRIPTION: TEST_VALUE, AMOUNT: 1000},
    }
    repository = ExpenseRepository(file_accessor=mock_accessor)
    updated_expense = Expense(UPDATED_TEST, 2000)

    repository.update(1, updated_expense)

    mock_accessor.write.assert_called_once()
    written_data = mock_accessor.write.call_args[0][0]

    assert written_data[ID_ONE][DESCRIPTION] == UPDATED_TEST
    assert written_data[ID_ONE][AMOUNT] == 2000


def test_delete_expense(mock_accessor: MagicMock) -> None:
    mock_accessor.read.return_value = {
        ID_ONE: {DESCRIPTION: EXPENSE_VALUE, AMOUNT: 1000},
    }
    repository = ExpenseRepository(file_accessor=mock_accessor)

    repository.delete(1)

    mock_accessor.write.assert_called_once()
    written_data = mock_accessor.write.call_args[0][0]

    assert ID_ONE not in written_data
