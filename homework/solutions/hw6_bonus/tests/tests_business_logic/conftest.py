import pytest
from unittest.mock import MagicMock
from solution.business_logic.budget import Budget
from typing import Any, Optional


def mocked_budget_init(
    self: Budget,
    income_repository: Optional[Any] = None,
    expense_repository: Optional[Any] = None
) -> None:
    mock_income_repo = MagicMock()
    mock_expense_repo = MagicMock()

    mock_income_repo.get_all.return_value = []
    mock_expense_repo.get_all.return_value = []

    self._income_repository = mock_income_repo
    self._expense_repository = mock_expense_repo
    self._income = self._income_repository.get_all()
    self._expense = self._expense_repository.get_all()


@pytest.fixture(autouse=True)
def mock_repositories(monkeypatch: Any) -> None:
    monkeypatch.setattr(Budget, "__init__", mocked_budget_init)
