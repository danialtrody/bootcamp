from unittest.mock import MagicMock
from solution.services.net_worth_service import NetWorth
from solution.models.account import Account
from solution.models.transaction import Transaction
import datetime
from decimal import Decimal


def test_calculate_net_worth_empty_data() -> None:
    mock_account_repo = MagicMock()
    mock_transaction_repo = MagicMock()
    mock_transfer_repo = MagicMock()

    mock_account_repo.get_all.return_value = []
    mock_transaction_repo.get_all.return_value = []

    service = NetWorth(mock_account_repo, mock_transaction_repo, mock_transfer_repo)
    result = service.calculate_net_worth()

    assert result == Decimal("0")


def test_calculate_net_worth_single_account_trans() -> None:

    mock_account_repo = MagicMock()
    mock_transaction_repo = MagicMock()
    mock_transfer_repo = MagicMock()

    mock_account_repo.get_all.return_value = [
        Account(id=1, name="Test", opening_balance=Decimal("100"))
    ]

    mock_transaction_repo.get_all.return_value = [
        Transaction(
            id=1,
            amount=Decimal("50"),
            date=datetime.date(2026, 1, 1),
            type="income",
            account_id=1,
            category_id=1,
        ),
        Transaction(
            id=2,
            amount=Decimal("20"),
            date=datetime.date(2026, 1, 1),
            type="expense",
            account_id=1,
            category_id=1,
        ),
    ]

    service = NetWorth(mock_account_repo, mock_transaction_repo, mock_transfer_repo)

    result = service.calculate_net_worth()

    assert result == Decimal("130")


def test_calculate_net_worth_multiple_accounts() -> None:
    mock_account_repo = MagicMock()
    mock_transaction_repo = MagicMock()
    mock_transfer_repo = MagicMock()

    mock_account_repo.get_all.return_value = [
        Account(id=1, name="A", opening_balance=Decimal("100")),
        Account(id=2, name="B", opening_balance=Decimal("100")),
    ]

    mock_transaction_repo.get_all.return_value = [
        Transaction(
            id=1,
            amount=Decimal("50"),
            date=datetime.date(2026, 1, 1),
            type="income",
            account_id=1,
            category_id=1,
        ),
        Transaction(
            id=1,
            amount=Decimal("10"),
            date=datetime.date(2026, 1, 1),
            type="expense",
            account_id=1,
            category_id=1,
        ),
        Transaction(
            id=2,
            amount=Decimal("10"),
            date=datetime.date(2026, 1, 2),
            type="expense",
            account_id=2,
            category_id=2,
        ),
    ]

    service = NetWorth(mock_account_repo, mock_transaction_repo, mock_transfer_repo)
    result = service.calculate_net_worth()
    expected = Decimal("230")

    assert result == expected


def test_calculate_net_worth_negative_balance() -> None:

    mock_account_repo = MagicMock()
    mock_transaction_repo = MagicMock()
    mock_transfer_repo = MagicMock()

    mock_account_repo.get_all.return_value = [
        Account(id=1, name="Test", opening_balance=Decimal("100"))
    ]

    mock_transaction_repo.get_all.return_value = [
        Transaction(
            id=1,
            amount=Decimal("200"),
            date=datetime.date(2026, 1, 1),
            type="expense",
            account_id=1,
            category_id=1,
        )
    ]

    service = NetWorth(mock_account_repo, mock_transaction_repo, mock_transfer_repo)

    result = service.calculate_net_worth()

    assert result == Decimal("-100")
