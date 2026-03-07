from unittest.mock import MagicMock

import pytest
from solution.services.account_service import AccountService
from solution.models.account import Account
from typing import List, Dict
from decimal import Decimal

TEST_ACCOUNT_NAME = "TEST"


def test_get_account_success() -> None:
    mock_repository = MagicMock()
    mock_transaction_repository = MagicMock()
    mock_transfer_repository = MagicMock()

    service = AccountService(
        mock_repository, mock_transaction_repository, mock_transfer_repository
    )

    expected_account = Account(id=1, name=TEST_ACCOUNT_NAME, opening_balance=Decimal("100"))

    mock_repository.get.return_value = expected_account

    result = service.get_account(1)

    assert result == expected_account
    mock_repository.get.assert_called_once_with(1)


@pytest.mark.parametrize(
    "test_data",
    [
        ([{"id": 1, "name": TEST_ACCOUNT_NAME, "opening_balance": "0"}]),
        (
            [
                {"id": 1, "name": TEST_ACCOUNT_NAME, "opening_balance": "100"},
                {"id": 2, "name": "TEST2", "opening_balance": "1"},
            ]
        ),
    ],
)
def test_get_all_accounts(test_data: List[Dict]) -> None:
    mock_repository = MagicMock()
    mock_transaction_repository = MagicMock()
    mock_transfer_repository = MagicMock()

    mock_repository.get_all.return_value = test_data

    service = AccountService(
        mock_repository, mock_transaction_repository, mock_transfer_repository
    )

    result = service.get_all_accounts()

    assert result == test_data
    mock_repository.get_all.assert_called_once()


@pytest.mark.parametrize(
    "test_data",
    [
        (Account(id=1, name=TEST_ACCOUNT_NAME, opening_balance=Decimal("10"))),
        (Account(id=2, name="TEST2", opening_balance=Decimal("200"))),
    ],
)
def test_add_account_succes(test_data: Account) -> None:
    mock_repository = MagicMock()
    mock_transaction_repository = MagicMock()
    mock_transfer_repository = MagicMock()

    mock_repository.create.return_value = test_data

    service = AccountService(
        mock_repository, mock_transaction_repository, mock_transfer_repository
    )

    result = service.add_account(test_data)

    assert result == test_data
    mock_repository.create.assert_called_once_with(test_data)


@pytest.mark.parametrize(
    "test_data, error",
    [
        (None, "Account cannot be None"),
        (
            Account(id=1, name="", opening_balance=Decimal("10")),
            "Account name cannot be empty",
        ),
    ],
)
def test_add_account_fail(test_data: Account, error: str) -> None:
    mock_repository = MagicMock()
    mock_transaction_repository = MagicMock()
    mock_transfer_repository = MagicMock()

    service = AccountService(
        mock_repository, mock_transaction_repository, mock_transfer_repository
    )

    with pytest.raises(ValueError, match=error):
        service.add_account(test_data)


def test_update_account_success() -> None:
    original_account = Account(id=1, name=TEST_ACCOUNT_NAME, opening_balance=Decimal("110"))

    updated_account = Account(id=1, name="UPDATED_TEST", opening_balance=Decimal("110"))

    mock_repository = MagicMock()
    mock_transaction_repository = MagicMock()
    mock_transfer_repository = MagicMock()

    service = AccountService(
        mock_repository, mock_transaction_repository, mock_transfer_repository
    )

    mock_repository.get.return_value = original_account
    mock_repository.update.return_value = updated_account

    result = service.update_account_name(1, "UPDATED_TEST")

    assert result == updated_account
    mock_repository.update.assert_called_once_with(updated_account)


def test_delete_account() -> None:
    mock_repository = MagicMock()
    mock_transaction_repository = MagicMock()
    mock_transfer_repository = MagicMock()

    service = AccountService(
        mock_repository, mock_transaction_repository, mock_transfer_repository
    )

    mock_repository.delete.return_value = None
    service.delete_account(1)

    mock_repository.delete.assert_called_once_with(1)


def test_get_account_balance() -> None:
    mock_account_repository = MagicMock()
    mock_transaction_repository = MagicMock()
    mock_transfer_repository = MagicMock()

    service = AccountService(
        mock_account_repository,
        mock_transaction_repository,
        mock_transfer_repository,
    )

    account = Account(id=1, name=TEST_ACCOUNT_NAME, opening_balance=Decimal("1000"))

    mock_account_repository.get.return_value = account

    mock_transaction_repository.get_all.return_value = []
    mock_transfer_repository.get_all.return_value = []

    result = service.get_account_balance(1)

    assert result == Decimal("1000")
