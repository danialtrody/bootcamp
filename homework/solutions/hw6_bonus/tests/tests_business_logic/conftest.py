import pytest
from unittest.mock import MagicMock
from solution.business_logic.budget import Budget

@pytest.fixture(autouse=True)
def mock_repositories(monkeypatch):
    mock_income_repo = MagicMock()
    mock_expense_repo = MagicMock()
    
    mock_income_repo.get_all.return_value = []
    mock_expense_repo.get_all.return_value = []
    
    def mocked_init(self, income_repository=None, expense_repository=None):
        self._income_repository = mock_income_repo
        self._expense_repository = mock_expense_repo
        self._income = self._income_repository.get_all()
        self._expense = self._expense_repository.get_all()
    monkeypatch.setattr(Budget, "__init__", mocked_init)