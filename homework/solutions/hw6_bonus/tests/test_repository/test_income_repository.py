import pytest
from unittest.mock import MagicMock
from solution.repository.income_repository import IncomeRepository
from solution.business_logic.income import Income


SALARY = "Salary"
SALARY_ONE = "Salary1"
SALARY_TWO = "Salary2"
UPDATED_SALARY = "Updated Salary"

ID_ONE = "1"
ID_TWO = "2"

DESCRIPTION = "description"
AMOUNT = "amount"


@pytest.fixture
def mock_accessor() -> MagicMock:
    mock = MagicMock()
    mock.read.return_value = {}
    return mock


def test_create_income(mock_accessor: MagicMock) -> None:
    repository = IncomeRepository(file_accessor=mock_accessor)
    income = Income(SALARY, 1000)

    repository.create(income)

    mock_accessor.read.assert_called_once()
    mock_accessor.write.assert_called_once()

    written_data = mock_accessor.write.call_args[0][0]

    assert ID_ONE in written_data
    assert written_data[ID_ONE][DESCRIPTION] == SALARY
    assert written_data[ID_ONE][AMOUNT] == 1000


def test_get_income(mock_accessor: MagicMock) -> None:
    mock_accessor.read.return_value = {
        ID_ONE: {DESCRIPTION: SALARY, AMOUNT: 1000},
    }
    repository = IncomeRepository(file_accessor=mock_accessor)

    income = repository.get(1)

    assert income.description == SALARY
    assert income.amount == 1000


def test_get_all_income(mock_accessor: MagicMock) -> None:
    mock_accessor.read.return_value = {
        ID_ONE: {DESCRIPTION: SALARY_ONE, AMOUNT: 1000},
        ID_TWO: {DESCRIPTION: SALARY_TWO, AMOUNT: 2000},
    }
    repository = IncomeRepository(file_accessor=mock_accessor)

    income = repository.get_all()

    assert len(income) == 2
    assert income[0].description == SALARY_ONE
    assert income[0].amount == 1000
    assert income[1].description == SALARY_TWO
    assert income[1].amount == 2000


def test_update_income(mock_accessor: MagicMock) -> None:
    mock_accessor.read.return_value = {
        ID_ONE: {DESCRIPTION: SALARY, AMOUNT: 1000},
    }
    repository = IncomeRepository(file_accessor=mock_accessor)
    updated_income = Income(UPDATED_SALARY, 2000)

    repository.update(1, updated_income)

    mock_accessor.write.assert_called_once()
    written_data = mock_accessor.write.call_args[0][0]

    assert written_data[ID_ONE][DESCRIPTION] == UPDATED_SALARY
    assert written_data[ID_ONE][AMOUNT] == 2000


def test_delete_income(mock_accessor: MagicMock) -> None:
    mock_accessor.read.return_value = {
        ID_ONE: {DESCRIPTION: SALARY, AMOUNT: 1000},
    }

    repo = IncomeRepository(file_accessor=mock_accessor)

    repo.delete(1)

    mock_accessor.write.assert_called_once()
    written_data = mock_accessor.write.call_args[0][0]

    assert ID_ONE not in written_data
